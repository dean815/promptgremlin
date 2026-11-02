import contextlib
import csv
import datetime as dt
import io
import json
import sys
import tempfile
from pathlib import Path

import build_scoreboard as B

FIX = Path(__file__).resolve().parent / "fixtures" / "scoreboard"
TODAY = dt.date(2026, 10, 27)
ALIASES = json.loads(B.ALIASES_PATH.read_text(encoding="utf-8"))


def _rows(config):
    return B.arena_rows(config, fixtures=FIX)


# Every recorded spelling of an aliased model, per source: a name maps exactly when it is listed here.
FIXTURE_SPELLINGS = {
    "lmarena": {
        "claude-fable-5-1": ["Claude Fable 5.1 (Max)", "claude-fable-5.1-max", "claude-fable-5.1-high"],
        "claude-opus-5-5": ["Claude Opus 5.5 (Max)", "Claude Opus 5.5 (High)", "claude-opus-5.5-medium"],
        "claude-sonnet-5-5": ["Claude Sonnet 5.5 (Max)", "Claude Sonnet 5.5 (High)", "Claude Sonnet 5.5 (xHigh)"],
        "claude-haiku-5-5": ["Claude Haiku 5.5 (High)"],
        "claude-fable-5": ["Claude Fable 5 (High)", "claude-fable-5", "claude-fable-5-high"],
        "claude-opus-5": ["Claude Opus 5 (Max)", "Claude Opus 5 (High)", "claude-opus-5-high"],
        "claude-sonnet-5": ["Claude Sonnet 5 (High)", "claude-sonnet-5-high", "claude-sonnet-5-search"],
        "gpt-6-astra": ["GPT-6 Astra (Max)", "gpt-6-astra-max"],
        "gpt-6-1-sol": ["GPT-6.1 Sol (Max)", "gpt-6.1-sol-max"],
        "gpt-6-luna": ["GPT-6 Luna (Max)", "GPT-6 Luna (Low)", "gpt-6-luna-max"],
        "gpt-6-sol": ["GPT-6 Sol (Max)", "gpt-6-sol-max"],
        "gpt-5-6-sol": ["GPT-5.6 Sol (xHigh)", "gpt-5.6-sol-xhigh"],
        "gpt-5-6-luna": ["gpt-5.6-luna-xhigh"],
        "gemini-3-8-flash": ["Gemini 3.8 Flash (High)"],
        "gemini-3-7-flash": ["Gemini 3.7 Flash (High)"],
        "gemini-3-6-flash": ["Gemini 3.6 Flash (High)", "gemini-3.6-flash-high"],
        "gemini-3-5-flash": ["Gemini 3.5 Flash (High)", "Gemini 3.5 Flash (Medium)",
                             "gemini-3.5-flash-high", "gemini-3.5-flash-medium"],
        "gemini-3-5-flash-lite": ["Gemini 3.5 Flash-Lite"],
        "gemini-3-1-pro-preview": ["Gemini 3.1 Pro Preview", "gemini-3.1-pro-preview", "gemini-3.1-pro-grounding"],
        "gemini-3-pro": ["Gemini 3 Pro", "gemini-3-pro-grounding"],
        "gemini-3-flash-preview": ["gemini-3-flash-grounding"],
        "grok-4-7": ["Grok 4.7 (xHigh)"],
        "grok-4-6": ["Grok 4.6 (xHigh)", "grok-4.6-high"],
        "glm-5-3": ["GLM-5.3 (Max)"],
        "glm-5-3-flash": ["GLM-5.3-Flash"],
        "glm-5-2": ["GLM-5.2 (Max)"],
        "qwen3-8-max": ["Qwen3.8-Max", "Qwen3.8-Max (0902)", "qwen3.8-max"],
        "qwen3-7-plus": ["Qwen3.7-Plus", "qwen3.7-plus"],
        "qwen3-7-max": ["Qwen3.7-Max-Preview"],
        "deepseek-v4-pro": ["DeepSeek-V4-Pro", "DeepSeek-V4-Pro (High, 20260813)"],
        "deepseek-flash": ["DeepSeek-V4.1-Flash-20260910 (Max)", "DeepSeek-V4.1-Flash-20261017 (Max)"],
        "mistral-large-4": ["Mistral Large 4"],
        "mistral-medium-3-5": ["Mistral Medium 3.5"],
        "mistral-large-3": ["Mistral Large 3"],
        "muse-wonder-1-0": ["Muse Wonder (Max)"],
        "muse-spark-1-3": ["Muse Spark 1.3 (Max)", "Muse Spark 1.3 (xHigh)", "muse-spark-1.3-max"],
        "muse-spark-1-2": ["Muse Spark 1.2 (xHigh)"],
        "muse-spark-1-1": ["Muse Spark 1.1", "muse-spark-1.1"],
        "muse-glimmer": ["Muse Glimmer"],
        "kimi-k3": ["Kimi K3 (Max)"],
        "kimi-k2-7-code": ["Kimi K2.7 Code"],
        "kimi-k2-6": ["Kimi K2.6", "kimi-k2.6"],
        "gpt-image-2-5-sunburst": ["GPT-Image-2.5 Sunburst"],
        "gpt-image-2-5-flare": ["GPT-Image-2.5 Flare"],
        "gpt-image-2": ["GPT-Image-2 (Medium)"],
        "gemini-nano-banana-2-1": ["Gemini Nano Banana 2.1"],
        "gemini-3-pro-image": ["Gemini 3 Pro Image (nano-banana-pro, 2K)",
                               "Gemini 3 Pro Image Preview (nano-banana-pro)"],
        "gemini-3-1-flash-image": ["Gemini 3.1 Flash Image (nano-banana-2, Web Search)"],
        "gemini-3-1-flash-lite-image": ["Gemini 3.1 Flash-Lite Image (nano-banana-2-lite)"],
        "gemini-omni-1-1-flash": ["gemini-omni-1.1-flash"],
        "veo-3-1-generate-preview": ["veo-3.1-audio", "veo-3.1-audio-1080p"],
        "veo-3-1-fast-generate-preview": ["veo-3.1-fast-audio", "veo-3.1-fast-audio-1080p"],
        "sora-2": ["sora-2"],
        "sora-2-pro": ["sora-2-pro"],
    },
    "epoch": {
        "claude-opus-5-5": ["Claude Opus 5.5"], "claude-fable-5-1": ["Claude Fable 5.1"],
        "claude-sonnet-5-5": ["Claude Sonnet 5.5"], "claude-haiku-5-5": ["Claude Haiku 5.5"],
        "claude-opus-5": ["Claude Opus 5"], "claude-fable-5": ["Claude Fable 5"],
        "claude-sonnet-5": ["Claude Sonnet 5"],
        "gpt-6-astra": ["GPT-6 Astra"], "gpt-6-1-sol": ["GPT-6.1 Sol"], "gpt-6-luna": ["GPT-6 Luna"],
        "gpt-6-sol": ["GPT-6 Sol"], "gpt-5-6-sol": ["GPT-5.6 Sol"], "gpt-5-6-luna": ["GPT-5.6 Luna"],
        "gemini-3-8-flash": ["Gemini 3.8 Flash"], "gemini-3-7-flash": ["Gemini 3.7 Flash"],
        "gemini-3-6-flash": ["Gemini 3.6 Flash"], "gemini-3-5-flash-lite": ["Gemini 3.5 Flash-Lite"],
        "gemini-3-1-flash-lite": ["Gemini 3.1 Flash-Lite"],
        "grok-4-7": ["Grok 4.7"], "grok-4-6": ["Grok 4.6"],
        "glm-5-3": ["GLM-5.3"], "glm-5-3-flash": ["GLM-5.3-Flash"], "glm-5-2": ["GLM-5.2"],
        "qwen3-8-max": ["Qwen 3.8 Max"], "qwen3-7-plus": ["Qwen3.7-Plus"],
        "deepseek-v4-pro": ["DeepSeek-V4-Pro"],
        "mistral-large-4": ["Mistral Large 4"], "mistral-medium-3-5": ["Mistral Medium 3.5"],
        "muse-wonder-1-0": ["Muse Wonder"], "muse-spark-1-3": ["Muse Spark 1.3"],
        "muse-spark-1-2": ["Muse Spark 1.2"], "muse-spark-1-1": ["Muse Spark 1.1"],
        "kimi-k3": ["Kimi K3"], "kimi-k2-7-code": ["Kimi K2.7 Code"], "kimi-k2-6": ["Kimi K2.6"],
    },
    "models.dev": {
        "mistral-large-4": ["mistral-large-4"], "qwen3-8-max": ["qwen3.8-max"],
        "qwen3-8-flash": ["qwen3.8-flash"], "grok-4-7": ["grok-4.7"], "gpt-6-1-sol": ["gpt-6.1-sol"],
        "gpt-6-astra": ["gpt-6-astra"], "gpt-6-luna": ["gpt-6-luna"], "gemini-3-6-flash": ["gemini-3.6-flash"],
        "gemini-3-5-flash-lite": ["gemini-3.5-flash-lite"], "gemini-3-8-flash": ["gemini-3.8-flash"],
        "kimi-k3": ["kimi-k3"], "kimi-k2-7-code": ["kimi-k2.7-code"], "kimi-k2-6": ["kimi-k2.6"],
        "claude-sonnet-5-5": ["claude-sonnet-5-5"], "claude-haiku-5-5": ["claude-haiku-5-5"],
        "claude-fable-5-1": ["claude-fable-5-1"], "claude-opus-5-5": ["claude-opus-5-5"],
        "muse-wonder-1-0": ["muse-wonder-1.0"], "muse-spark-1-3": ["muse-spark-1.3"],
        "muse-spark-1-1": ["muse-spark-1.1"], "muse-spark-1-2": ["muse-spark-1.2"],
        "glm-5-3-flashx": ["glm-5.3-flashx"], "glm-5-2": ["glm-5.2"], "glm-5-3-flash": ["glm-5.3-flash"],
        "glm-5-3": ["glm-5.3"], "deepseek-v4-pro": ["deepseek-v4-pro"], "deepseek-flash": ["deepseek-flash"],
    },
    "openrouter": {
        "claude-haiku-5-5": ["anthropic/claude-haiku-5.5"], "claude-sonnet-5-5": ["anthropic/claude-sonnet-5.5"],
        "claude-opus-5-5": ["anthropic/claude-opus-5.5"], "claude-fable-5-1": ["anthropic/claude-fable-5.1"],
        "gpt-6-1-sol": ["openai/gpt-6.1-sol"], "gpt-6-luna": ["openai/gpt-6-luna"],
        "gpt-6-astra": ["openai/gpt-6-astra"], "grok-4-7": ["x-ai/grok-4.7"],
        "glm-5-3-flashx": ["z-ai/glm-5.3-flashx"], "glm-5-3-flash": ["z-ai/glm-5.3-flash"],
        "glm-5-3": ["z-ai/glm-5.3"], "glm-5-2": ["z-ai/glm-5.2"],
        "muse-spark-1-3": ["meta/muse-spark-1.3"], "muse-spark-1-2": ["meta/muse-spark-1.2"],
        "muse-spark-1-1": ["meta/muse-spark-1.1"], "gemini-3-8-flash": ["google/gemini-3.8-flash"],
        "gemini-3-6-flash": ["google/gemini-3.6-flash"], "gemini-3-5-flash-lite": ["google/gemini-3.5-flash-lite"],
        "gemini-3-1-flash-lite": ["google/gemini-3.1-flash-lite"],
        "gemini-3-1-pro-preview": ["google/gemini-3.1-pro-preview"],
        "gemini-3-flash-preview": ["google/gemini-3-flash-preview"], "qwen3-8-flash": ["qwen/qwen3.8-flash"],
        "qwen3-7-plus": ["qwen/qwen3.7-plus"], "kimi-k3": ["moonshotai/kimi-k3"],
        "kimi-k2-7-code": ["moonshotai/kimi-k2.7-code"], "kimi-k2-6": ["moonshotai/kimi-k2.6"],
        "mistral-medium-3-5": ["mistralai/mistral-medium-3-5"], "deepseek-v4-pro": ["deepseek/deepseek-v4-pro"],
    },
    "litellm": {
        "gpt-6-astra": ["azure/gpt-6-astra", "gpt-6-astra"], "gpt-6-luna": ["azure/gpt-6-luna", "gpt-6-luna"],
        "gpt-6-1-sol": ["azure/gpt-6.1-sol", "gpt-6.1-sol"],
        "claude-sonnet-5-5": ["claude-sonnet-5-5"], "claude-fable-5-1": ["claude-fable-5-1"],
        "claude-opus-5-5": ["claude-opus-5-5"], "claude-haiku-5-5": ["claude-haiku-5-5"],
        "deepseek-v4-pro": ["dashscope/deepseek-v4-pro", "deepseek-v4-pro", "deepseek/deepseek-v4-pro"],
        "deepseek-flash": ["deepseek-flash", "deepseek/deepseek-flash"],
        "glm-5-2": ["dashscope/glm-5.2", "mistral/glm-5-2", "zai/glm-5.2"],
        "glm-5-3": ["zai/glm-5.3"], "glm-5-3-flash": ["zai/glm-5.3-flash"],
        "kimi-k2-7-code": ["dashscope/kimi-k2.7-code", "moonshot/kimi-k2.7-code"],
        "kimi-k2-6": ["moonshot/kimi-k2.6"], "kimi-k3": ["moonshot/kimi-k3"],
        "qwen3-7-plus": ["dashscope/qwen3.7-plus"], "qwen3-8-max": ["dashscope/qwen3.8-max"],
        "qwen3-8-flash": ["dashscope/qwen3.8-flash"],
        "gemini-3-1-flash-lite": ["gemini/gemini-3.1-flash-lite"],
        "gemini-3-5-flash-lite": ["gemini/gemini-3.5-flash-lite"],
        "gemini-3-flash-preview": ["gemini/gemini-3-flash-preview"], "gemini-3-6-flash": ["gemini/gemini-3.6-flash"],
        "gemini-3-8-flash": ["gemini/gemini-3.8-flash"], "gemini-3-1-pro-preview": ["gemini/gemini-3.1-pro-preview"],
        "mistral-large-4": ["mistral/mistral-large-4"], "mistral-large-3": ["mistral/mistral-large-3"],
        "mistral-medium-3-5": ["mistral/mistral-medium-3-5", "mistral/mistral-medium-3.5"],
        "grok-4-7": ["xai/grok-4.7"],
    },
}


def _fixture_names(source):
    if source == "lmarena":
        return {r["model_name"] for f in FIX.glob("arena_*.json") for r in json.loads(f.read_text())}
    if source == "epoch":
        return {r["Model"] for r in csv.DictReader(io.StringIO((FIX / "epoch_eci.csv").read_text()))}
    if source == "models.dev":
        return {m for p in json.loads((FIX / "models_dev.json").read_text()).values() for m in p["models"]}
    if source == "openrouter":
        return {e["id"] for e in json.loads((FIX / "openrouter.json").read_text())["data"]}
    return set(json.loads((FIX / "litellm.json").read_text()))


def test_fixture_spellings_map_exactly():
    """Each recorded name of a model we alias maps to it, and nothing else maps at all."""
    for source, table in FIXTURE_SPELLINGS.items():
        want = {n: mid for mid, ns in table.items() for n in ns}
        present = _fixture_names(source)
        assert set(want) <= present, (source, sorted(set(want) - present))
        got = {n: B.names.canonical(source, n, ALIASES) for n in present}
        assert {n: m for n, m in got.items() if m} == want, source


def test_every_note_model_in_the_fixtures_is_aliased():
    """A family note id spelled in any recorded source is in the table above, so it maps."""
    listed = {mid for table in FIXTURE_SPELLINGS.values() for mid in table}
    recorded = {B.lineup.norm_id(B.names.split_effort(n)[0])
                for s in FIXTURE_SPELLINGS for n in _fixture_names(s)}
    for key, ids in B.family_note_ids().items():
        for mid in ids:
            assert ALIASES[mid]["family"] == key, mid
            assert mid not in recorded or mid in listed, mid


def test_import_needs_no_pyarrow():
    """The module imported above; pyarrow loads only inside the live parquet reader."""
    assert "pyarrow" not in sys.modules


def test_arena_webdev_metrics_scales_and_unmapped():
    metrics, scales, unmapped, published = B.arena_metrics("webdev", _rows("webdev"), ALIASES)
    rows = metrics["claude-opus-5-5"]["lmarena:webdev"]
    top = next(r for r in rows if r["effort"] == "max")
    assert top["elo"] == 1809 and top["lo"] == 1796 and top["hi"] == 1822 and top["votes"] == 3451
    assert len([r for r in rows if r["effort"] == "max"]) == 1   # overall and webdev rows are one board
    b = scales["lmarena:webdev"]
    # The 30th distinct model, though every model is listed under both categories.
    overall = sorted((r["rating"] for r in _rows("webdev") if r["category"] == "overall"), reverse=True)
    assert b == {"top": 1809, "p30": round(overall[29])}
    assert not [k for k in scales if k.startswith("lmarena:webdev/")]   # trimmed fixture: main board only
    assert unmapped and not any(B.names.canonical("lmarena", n, ALIASES) for n, _ in unmapped)
    assert all(isinstance(v, (int, float)) for _, v in unmapped)
    assert published == "2026-10-27"


def test_unmapped_window_counts_distinct_models():
    rows = [{"model_name": f"Unknown {i}", "rating": 1800 - i, "rating_lower": 1790 - i,
             "rating_upper": 1810 - i, "vote_count": 100, "category": cat,
             "leaderboard_publish_date": "2026-10-27"}
            for i in range(40) for cat in ("overall", "webdev")]
    _, scales, unmapped, _ = B.arena_metrics("webdev", rows, ALIASES)
    assert len(unmapped) == B.TOP_N and scales["lmarena:webdev"] == {"top": 1800, "p30": 1771}
    assert unmapped[0] == ("Unknown 0", 1800)


def test_unmapped_flags_carry_the_rating():
    snap = B.build(_inputs(), ALIASES, [], TODAY)
    unmapped = [f for f in snap["flags"] if f.startswith("UNMAPPED")]
    assert unmapped and all(f.rsplit(" @", 1)[1].replace(".", "").isdigit() for f in unmapped)


def test_arena_categories_get_their_own_keys():
    metrics, scales, _, published = B.arena_metrics("text", _rows("text"), ALIASES)
    assert {"lmarena:text", "lmarena:text/coding", "lmarena:text/creative_writing"} <= set(scales)
    assert "lmarena:text/creative_writing" in metrics["claude-opus-5-5"]
    assert published == "2026-10-22"


def test_arena_agent_reads_score_fields():
    metrics, scales, _, _ = B.arena_metrics("agent", _rows("agent"), ALIASES)
    row = next(r for r in metrics["claude-opus-5-5"]["lmarena:agent"] if r["effort"] == "max")
    assert set(row) == {"effort", "score", "lo", "hi"}
    assert 0.2 < row["score"] < 0.21 and row["lo"] < row["score"] < row["hi"]
    assert scales["lmarena:agent"]["top"] == row["score"]


def test_livebench_release():
    assert B.livebench_release('a;Yt=["20261014","20261025"],Zt=1') == "20261025"
    assert B.livebench_release('var x=["2024-06-24","2026-06-25"];') is None
    assert B.livebench_release((FIX / "livebench_bundle.js").read_text()) == "20261025"


def test_epoch_eci_maps_display_names():
    out = B.epoch_eci((FIX / "epoch_eci.csv").read_text(encoding="utf-8"), ALIASES)
    assert out["claude-opus-5-5"] == {"score": 168.83, "lo": 165.25, "hi": 173.95}
    assert out["claude-opus-5"] != out["claude-opus-5-5"]   # Opus 5 keeps its own row


def test_epoch_board_scale_comes_from_the_whole_index():
    text = (FIX / "epoch_eci.csv").read_text(encoding="utf-8")
    scores = sorted((float(r["eci"]) for r in csv.DictReader(io.StringIO(text)) if r["eci"]), reverse=True)
    assert B.epoch_scale(text) == {"top": 168.83, "p30": scores[29]}
    snap = B.build(_inputs(), ALIASES, [], TODAY)
    assert snap["boards"]["epoch:eci"] == B.epoch_scale(text)
    failed = B.build(_inputs(epoch=_boom), ALIASES, [], TODAY, snap)
    assert failed["boards"]["epoch:eci"] == snap["boards"]["epoch:eci"]


def test_blank_or_null_intervals_keep_the_score():
    out = B.epoch_eci("Model,eci,eci_ci_low,eci_ci_high,model_versions\nClaude Opus 5.5,168.83,,173.95,\n",
                      ALIASES)
    assert out["claude-opus-5-5"] == {"score": 168.83, "lo": None, "hi": 173.95}
    row = {"model_name": "Claude Opus 5.5 (Max)", "rating": 1809.4, "rating_lower": None,
           "rating_upper": 1822.1, "vote_count": None, "category": "overall",
           "leaderboard_publish_date": "2026-10-27"}
    metrics, _, _, _ = B.arena_metrics("webdev", [row], ALIASES)
    assert metrics["claude-opus-5-5"]["lmarena:webdev"] == [
        {"effort": "max", "elo": 1809, "lo": None, "hi": 1822, "votes": None}]


def test_unparseable_source_fails_alone_and_carries_previous():
    prev = B.build(_inputs(), ALIASES, [], TODAY)
    bad = lambda: [{"model_name": "x"}]  # noqa: E731  (no rating column at all)
    snap = B.build(_inputs(**{"lmarena:search": bad, "epoch": lambda: ("no,columns\n1,2\n", "x", "y")}),
                   ALIASES, [], TODAY, prev)
    assert {"SOURCE-FAIL lmarena:search", "SOURCE-FAIL epoch"} <= set(snap["flags"])
    opus, was = snap["models"]["claude-opus-5-5"]["metrics"], prev["models"]["claude-opus-5-5"]["metrics"]
    assert opus["lmarena:search"] == was["lmarena:search"] and opus["epoch:eci"] == was["epoch:eci"]
    assert snap["sources"]["epoch"] == prev["sources"]["epoch"]


A = {"m": {"family": "x"}, "gemini-4-argon": {"family": "gemini"}}


def test_prices_majority_and_mismatch():
    md = {"x": {"models": {"m": {"id": "m", "cost": {"input": 2, "output": 10},
                                 "canonical_model_id": "x/m"}}}}
    ll = {"m": {"litellm_provider": "x", "input_cost_per_token": 4e-06, "output_cost_per_token": 2e-05}}
    orr = {"data": [{"id": "x/m", "pricing": {"prompt": "0.000004", "completion": "0.00002"}}]}
    price, flags = B.prices(md, ll, orr, A, [], TODAY, first_party={"x": "x"})
    assert price["m"] == {"in": 4.0, "out": 20.0, "from": "majority"}
    assert flags == ["PRICE-MISMATCH m"]


def test_prices_single_catalog_and_resellers_ignored():
    # Azure resells it; vendor y's own API hosts it too, but y is not the model's vendor.
    ll = {"azure/m": {"litellm_provider": "azure", "input_cost_per_token": 9e-06,
                      "output_cost_per_token": 9e-05},
          "y/m": {"litellm_provider": "y", "input_cost_per_token": 8e-06, "output_cost_per_token": 8e-05}}
    md = {"x": {"models": {"m": {"id": "m", "cost": {"input": 2, "output": 10},
                                 "canonical_model_id": "x/m"}}},
          "reseller": {"models": {"m": {"id": "m", "cost": {"input": 7, "output": 70},
                                        "canonical_model_id": "x/m"}}}}
    price, flags = B.prices(md, ll, {"data": []}, A, [], TODAY, first_party={"x": "x", "y": "y"})
    assert price["m"] == {"in": 2.0, "out": 10.0, "from": "models.dev"} and flags == []


def test_litellm_first_party_keys_with_version_dots_count():
    """LiteLLM agrees with OpenRouter on GLM-5.3 Flash (0.15/0.5) against models.dev's figure."""
    load = lambda name: json.loads((FIX / name).read_text(encoding="utf-8"))  # noqa: E731
    price, _ = B.prices(load("models_dev.json"), load("litellm.json"), load("openrouter.json"),
                        ALIASES, [], TODAY)
    assert price["glm-5-3-flash"] == {"in": 0.15, "out": 0.5, "from": "majority"}
    assert price["kimi-k2-6"]["from"] == "majority"


def test_prices_schedule_in_force_and_future():
    orr = {"data": [{"id": "google/gemini-4-argon", "pricing": {"prompt": "0.000002", "completion": "0.00001"}}]}
    sched = [{"model": "gemini-4-argon", "from": "2026-12-01", "in": 4.0, "out": 20.0}]
    price, flags = B.prices({}, {}, orr, A, sched, TODAY)
    assert price["gemini-4-argon"] == {"in": 2.0, "out": 10.0, "from": "openrouter"}
    assert flags == ["PRICE-CHANGE gemini-4-argon 2026-12-01"]
    price, flags = B.prices({}, {}, orr, A, sched, dt.date(2026, 12, 1))
    assert price["gemini-4-argon"] == {"in": 4.0, "out": 20.0, "from": "schedule 2026-12-01"}
    assert flags == []


def test_efforts_levels_from_models_dev_default_from_openrouter():
    md = json.loads((FIX / "models_dev.json").read_text())
    orr = json.loads((FIX / "openrouter.json").read_text())
    e = B.efforts(md, orr, ALIASES)["claude-opus-5-5"]
    assert e == {"levels": ["low", "medium", "high", "xhigh", "max"], "default": "high",
                 "default_from": "openrouter"}


def _inputs(**override):
    inp = B.gather(FIX)
    inp.update(override)
    return inp


def _boom():
    raise OSError("down")


def test_build_from_fixtures():
    snap = B.build(_inputs(), ALIASES, [], TODAY)
    assert snap["version"] == 1
    assert snap["sources"]["lmarena"]["licence"] == "CC BY 4.0"
    assert snap["sources"]["livebench"]["release"] == "20261025"
    opus = snap["models"]["claude-opus-5-5"]
    assert opus["family"] == "anthropic" and opus["price"]["in"] == 4.0
    assert "epoch:eci" in opus["metrics"] and "lmarena:text" in opus["metrics"]
    assert set(snap["models"]) == set(ALIASES)


def test_build_carries_failed_source_from_previous():
    prev = B.build(_inputs(), ALIASES, [], TODAY)
    prev["models"]["claude-opus-5-5"]["metrics"]["lmarena:document"] = [{"effort": None, "elo": 1500}]
    snap = B.build(_inputs(**{"lmarena:document": _boom}), ALIASES, [], TODAY, prev)
    assert "SOURCE-FAIL lmarena:document" in snap["flags"]
    assert snap["models"]["claude-opus-5-5"]["metrics"]["lmarena:document"] == [{"effort": None, "elo": 1500}]
    assert snap["sources"]["lmarena"]["published"]["document"] == prev["sources"]["lmarena"]["published"]["document"]


def test_stale_board_flagged():
    snap = B.build(_inputs(), ALIASES, [], TODAY)
    assert "SOURCE-STALE lmarena:document 2026-09-13" in snap["flags"]
    assert not any(f.startswith("SOURCE-STALE lmarena:webdev") for f in snap["flags"])


# The notes' flagships when the fixtures were recorded. Frozen, so a notes refresh that adds a
# model the recordings never saw doesn't fail this test; the live check runs in the builder.
RECORDED_FLAGSHIPS = {
    "anthropic": "claude-fable-5-1", "openai": "gpt-6-astra", "gemini": "gemini-3-8-flash", "xai": "grok-4-7",
    "zhipu": "glm-5-3", "qwen": "qwen3-8-max", "deepseek": "deepseek-v4-pro", "mistral": "mistral-large-4",
    "meta": "muse-wonder-1-0", "kimi": "kimi-k3"}


def test_fixture_build_with_real_aliases_validates():
    snap = B.build(_inputs(), ALIASES, [], TODAY)
    assert B.validate(snap, RECORDED_FLAGSHIPS, snap) == []
    spelled = {n for table in FIXTURE_SPELLINGS.values() for ns in table.values() for n in ns}
    assert not [f for f in snap["flags"] if f.startswith("UNMAPPED") and f.split(" ", 2)[2].rsplit(" @", 1)[0] in spelled]


def test_validate_rejects_missing_flagship_and_changed_licence():
    snap = B.build(_inputs(), ALIASES, [], TODAY)
    flagships = {"anthropic": "claude-fable-5-1", "openai": "gpt-6-astra"}
    assert B.validate(snap, flagships, snap) == []
    assert any("nope-1" in e for e in B.validate(snap, {"x": "nope-1"}))
    prev = json.loads(json.dumps(snap))
    prev["sources"]["epoch"]["licence"] = "CC BY-NC 4.0"
    assert any("licence" in e for e in B.validate(snap, flagships, prev))
    few = {k: ALIASES[k] for k in ("claude-opus-5-5", "gpt-6-astra", "claude-fable-5-1")}
    thin = B.build(_inputs(), few, [], TODAY)
    assert any("lmarena:text" in e for e in B.validate(thin, flagships))


def test_cli_fixture_build_writes_no_livebench_metrics():
    out = Path(tempfile.mkdtemp()) / "sb.json"
    with contextlib.redirect_stdout(io.StringIO()):
        assert B.main(["--fixtures", str(FIX), "--out", str(out), "--today", "2026-10-27"]) == 0
    text = out.read_text(encoding="utf-8")
    snap = json.loads(text)
    assert "livebench:" not in text
    assert snap["models"]["claude-opus-5-5"]["metrics"]


def test_fixtures_are_small_and_hold_no_livebench_csv():
    files = list(FIX.iterdir())
    assert sum(f.stat().st_size for f in files) < 100_000
    assert not [f for f in files if f.suffix == ".csv" and "livebench" in f.name]
