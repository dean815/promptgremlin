import json
import re
from pathlib import Path

from pglib import names as N
from pglib import registry

SKILL = Path(__file__).resolve().parents[2]

ALIASES = {
    "claude-opus-5-5": {"family": "anthropic",
                        "names": {"lmarena": ["Claude Opus 5.5", "claude-opus-5.5"],
                                  "openrouter": ["anthropic/claude-opus-5.5"]}},
    "claude-opus-5": {"family": "anthropic", "names": {"lmarena": ["Claude Opus 5"]}},
    "claude-sonnet-5-5": {"family": "anthropic", "names": {"lmarena": ["Sonnet 5.5"]}},
    "gpt-6-1-sol": {"family": "openai", "names": {"lmarena": ["gpt-5.6-sol"]},
                    "patterns": {"search": ["^gpt-6-1-sol(-search)?$"]}},
    "qwen3-8-max": {"family": "qwen", "names": {"lmarena": ["qwen3.8-max"]}},
}


def test_split_effort_brackets_and_suffixes():
    assert N.split_effort("Claude Opus 5.5 (High)") == ("Claude Opus 5.5", "high")
    assert N.split_effort("Sonnet 5.5 (xHigh)") == ("Sonnet 5.5", "xhigh")
    assert N.split_effort("claude-opus-5-high") == ("claude-opus-5", "high")
    assert N.split_effort("gpt-5.6-sol-xhigh") == ("gpt-5.6-sol", "xhigh")
    assert N.split_effort("claude-fable-5-1_max") == ("claude-fable-5-1", "max")
    assert N.split_effort("Kimi K3 (Thinking)") == ("Kimi K3", "thinking")
    assert N.split_effort("GPT-6 Luna (Minimal)") == ("GPT-6 Luna", "minimal")
    assert N.split_effort("gemini-omni-1.1-flash") == ("gemini-omni-1.1-flash", None)


def test_split_effort_live_bracket_extras():
    # Arena packs harness, budget and date into the same bracket as the effort.
    assert N.split_effort("GPT-5.6 Sol (xHigh, Codex Harness)") == ("GPT-5.6 Sol", "xhigh")
    assert N.split_effort("Claude Opus 4.5 (High, 32K, 20251101)") == ("Claude Opus 4.5", "high")
    assert N.split_effort("Claude Opus 4 (Thinking 16K, 20250514)") == ("Claude Opus 4", "thinking")
    assert N.split_effort("Claude Haiku 4.5 (20251001)") == ("Claude Haiku 4.5 (20251001)", None)


def test_canonical_maps_display_names_slugs_and_router_ids():
    assert N.canonical("lmarena", "Claude Opus 5.5 (Max)", ALIASES) == "claude-opus-5-5"
    assert N.canonical("lmarena", "claude-opus-5.5-medium", ALIASES) == "claude-opus-5-5"
    assert N.canonical("openrouter", "anthropic/claude-opus-5.5", ALIASES) == "claude-opus-5-5"
    assert N.canonical("lmarena", "Sonnet 5.5 (xHigh)", ALIASES) == "claude-sonnet-5-5"
    assert N.canonical("lmarena", "gpt-5.6-sol-xhigh", ALIASES) == "gpt-6-1-sol"


def test_canonical_keeps_generations_apart():
    # On Arena's search and document boards "claude-opus-5-high" is Opus 5, not Opus 5.5.
    assert N.canonical("lmarena", "claude-opus-5-high", ALIASES) == "claude-opus-5"
    assert N.canonical("lmarena", "Claude Opus 5 (Max)", ALIASES) == "claude-opus-5"


def test_canonical_patterns_are_per_source():
    assert N.canonical("search", "gpt-6.1-sol-search", ALIASES) == "gpt-6-1-sol"
    assert N.canonical("lmarena", "gpt-6.1-sol-search", ALIASES) is None


def test_canonical_full_name_before_effort_split():
    # "-max" is part of Qwen's model name, not an effort.
    assert N.canonical("lmarena", "qwen3.8-max", ALIASES) == "qwen3-8-max"


def test_canonical_direct_id_and_unmapped():
    assert N.canonical("livebench", "claude-opus-5-5", ALIASES) == "claude-opus-5-5"
    assert N.canonical("livebench", "claude-opus-5.5", ALIASES) == "claude-opus-5-5"
    assert N.canonical("litellm", "openai/gpt-6.1-sol", ALIASES) == "gpt-6-1-sol"
    assert N.canonical("lmarena", "MiMo-V2.6-Pro", ALIASES) is None


def test_alias_file_is_valid():
    aliases = json.loads((SKILL / "model_aliases.json").read_text())
    reg = registry.load(SKILL / "sources.json")
    families = {k for k, e in reg.items() if e["kind"] == "family"}
    seen = {}
    for mid, e in aliases.items():
        assert mid == N.norm_id(mid), mid
        assert e["family"] in families, mid
        for source, names in e.get("names", {}).items():
            assert isinstance(names, list), (mid, source)
            for n in names:
                key = (source, N.norm_id(n))
                assert seen.setdefault(key, mid) == mid, f"{n} maps to {seen[key]} and {mid}"
        for pats in e.get("patterns", {}).values():
            assert isinstance(pats, list), mid
            for p in pats:
                re.compile(p)


def test_seed_maps_live_spellings():
    aliases = json.loads((SKILL / "model_aliases.json").read_text())
    cases = [("lmarena", "Claude Opus 5.5 (High)", "claude-opus-5-5"),
             ("lmarena", "Claude Sonnet 5.5 (xHigh)", "claude-sonnet-5-5"),
             ("lmarena", "claude-fable-5.1-max", "claude-fable-5-1"),
             ("lmarena", "GPT-6.1 Sol (Max)", "gpt-6-1-sol"),
             ("lmarena", "gpt-6-astra-max", "gpt-6-astra"),
             ("openrouter", "anthropic/claude-haiku-5.5", "claude-haiku-5-5"),
             ("openrouter", "openai/gpt-6-luna", "gpt-6-luna"),
             ("livebench", "gpt-6.1-sol", "gpt-6-1-sol")]
    for source, name, want in cases:
        assert N.canonical(source, name, aliases) == want, (source, name)
    # Previous generations never fold into the current model.
    assert N.canonical("lmarena", "claude-opus-5-high", aliases) != "claude-opus-5-5"
    assert N.canonical("lmarena", "GPT-6 Sol (Max)", aliases) != "gpt-6-1-sol"


def test_every_note_model_has_an_alias_entry():
    """Family note ids carry their own family; media tool ids carry their vendor's family."""
    aliases = json.loads((SKILL / "model_aliases.json").read_text())
    reg = registry.load(SKILL / "sources.json")
    ids = registry.note_ids_by_key(SKILL / "targets", reg)
    for key, e in reg.items():
        if e["kind"] == "family":
            for mid in ids.get(key, []):
                assert aliases.get(mid, {}).get("family") == key, mid
    media = {"nano-banana": "gemini", "google-video": "gemini", "gpt-image": "openai", "sora": "openai"}
    for key, fam in media.items():
        for mid in ids[key]:
            assert aliases.get(mid, {}).get("family") == fam, mid


def test_seed_maps_previews_dated_rows_and_router_suffixes():
    aliases = json.loads((SKILL / "model_aliases.json").read_text())
    cases = [("lmarena", "Gemini 3.1 Flash-Lite Preview", "gemini-3-1-flash-lite"),
             ("lmarena", "Qwen3.7-Max (20260517)", "qwen3-7-max"),
             ("lmarena", "DeepSeek-V4.1-Flash-20261017 (Max)", "deepseek-flash"),
             ("lmarena", "DeepSeek-V4-Flash (High)", "deepseek-v4-flash"),
             ("lmarena", "Claude Haiku 4.5 (20251001)", "claude-haiku-4-5"),
             ("lmarena", "veo-3.1-fast-audio-1080p", "veo-3-1-fast-generate-preview"),
             ("epoch", "Qwen3.8 Max (0902)", "qwen3-8-max"),
             ("epoch", "DeepSeek V4.1 Flash", "deepseek-flash"),
             ("openrouter", "deepseek/deepseek-v4.1-flash-1017", "deepseek-flash"),
             ("openrouter", "mistralai/mistral-large-4-0", "mistral-large-4"),
             ("openrouter", "meta/muse-wonder", "muse-wonder-1-0"),
             ("livebench", "deepseek-v4.1-flash-1017", "deepseek-flash"),
             ("livebench", "muse-wonder-1.0", "muse-wonder-1-0")]
    for source, name, want in cases:
        assert N.canonical(source, name, aliases) == want, (source, name)
    # Separate models that share a prefix stay out.
    for source, name in [("lmarena", "Muse Wonder Full (Max)"), ("lmarena", "Muse Spark"),
                         ("lmarena", "Qwen3.8-Flash-Next"), ("lmarena", "GPT-6.1 Terra (Max)"),
                         ("lmarena", "gemini-omni-flash"), ("lmarena", "veo-3-audio"),
                         ("openrouter", "qwen/qwen3.8-max-prime"), ("openrouter", "openai/gpt-6-sol-pro"),
                         ("openrouter", "meta/muse-spark-1.3-contributor"), ("lmarena", "Kimi K3.1 Pro (Max)")]:
        assert N.canonical(source, name, aliases) is None, (source, name)
