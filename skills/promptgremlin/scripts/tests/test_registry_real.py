from pathlib import Path

from pglib import registry

SKILL = Path(__file__).resolve().parents[2]
KEYS = ("anthropic openai gemini xai zhipu qwen deepseek mistral meta kimi claude-code codex "
        "gemini-cli cursor copilot lovable replit perplexity manus nano-banana gpt-image midjourney "
        "google-video sora runway kling higgsfield elevenlabs n8n gamma notion-ai jev grok-bot").split()


def test_real_registry_is_valid_and_complete():
    reg = registry.load(SKILL / "sources.json")
    assert registry.validate(reg) == []
    assert sorted(reg) == sorted(KEYS)


def test_every_family_has_a_lineup():
    reg = registry.load(SKILL / "sources.json")
    for key, e in reg.items():
        if e["kind"] == "family":
            assert e.get("lineup"), key


# One synthetic next-generation sample per target, written the way that vendor's page names models.
NEXT_GEN = {
    "anthropic": "claude-opus-6",
    "openai": "gpt-7-nova",
    "gemini": "gemini-4-flash",
    "xai": "grok-5",
    "zhipu": "| GLM-6",
    "qwen": "qwen4-max",
    "deepseek": "deepseek-v5-flash",
    "mistral": "Mistral Medium 4",
    "meta": "muse-spark-2.0",
    "kimi": "kimi-k4",
    "nano-banana": "gemini-4-flash-image",
    "gpt-image": "GPT Image 3 Flare",
    "midjourney": "## V9",
    "google-video": ["gemini-omni-2-flash", "veo-4-generate"],
    "sora": "sora-3",
    "runway": "gen-5",
    "elevenlabs": "Eleven v5",
    "jev": "jev-2.0.0",
}


def _specs(entry):
    lu = entry["lineup"]
    return lu if isinstance(lu, list) else [lu]


def test_lineup_regexes_catch_next_generation():
    import re
    reg = registry.load(SKILL / "sources.json")
    with_lineup = {k for k, e in reg.items() if e.get("lineup")}
    assert with_lineup == set(NEXT_GEN), with_lineup ^ set(NEXT_GEN)
    for key, sample in NEXT_GEN.items():
        samples = sample if isinstance(sample, list) else [sample]
        rxs = [re.compile(s["model_regex"], re.I) for s in _specs(reg[key])]
        for text in samples:
            text = "x\n" + text + "\ny"  # line-anchored patterns need their own line
            assert any(rx.search(text) for rx in rxs), (key, text)


def test_every_target_has_notes_with_all_models_block():
    from pglib import notes
    reg = registry.load(SKILL / "sources.json")
    for key in reg:
        n = notes.load(SKILL / "targets" / f"{key}.md")
        assert "All models" in n.blocks, key
        assert len(n.blocks["All models"]) <= 2800, (key, len(n.blocks["All models"]))
        assert len(n.blocks.get("Effort", "")) <= 600, key
        for mid in notes.model_ids(n):
            assert len(n.blocks[mid]) <= 800, (key, mid)
        assert n.meta.get("last_verified", "2000-01-01") != "2000-01-01", key


def test_combined_briefing_budget_notes_only():
    """Approximate briefing size for targets that use others: All models + Effort + the largest
    model block, for the target itself and for each target it uses. Must stay under 7,400 chars
    (the spec's report budget); the real report also adds a header, flags and section titles."""
    from pglib import notes
    reg = registry.load(SKILL / "sources.json")

    def part(key):
        n = notes.load(SKILL / "targets" / f"{key}.md")
        models = [len(n.blocks[m]) for m in notes.model_ids(n)]
        return (len(n.blocks.get("All models", "")) + len(n.blocks.get("Effort", ""))
                + max(models, default=0))

    checked = 0
    for key, e in reg.items():
        if e.get("uses"):
            total = part(key) + sum(part(u) for u in e["uses"])
            assert total < 7400, (key, total)
            checked += 1
    assert checked


def test_registry_has_no_ua_overrides():
    assert '"ua"' not in (SKILL / "sources.json").read_text()
