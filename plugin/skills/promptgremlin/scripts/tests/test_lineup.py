from pglib import lineup

PAGE = ("## Latest models\n| claude-fable-5-1 | x |\n| claude-opus-5-5 |\n"
        "| claude-haiku-4-5-20251001 |\n## Legacy models\n| claude-opus-4-1 |\n")
SPEC = {"model_regex": r"claude-(?:fable|opus|sonnet|haiku)-\d+(?:-\d{1,2})?(?!\d)",
        "section": "Latest models"}


def test_parse_scoped_to_section_and_strips_dates():
    assert lineup.parse(PAGE, SPEC) == ["claude-fable-5-1", "claude-opus-5-5", "claude-haiku-4-5"]


def test_parse_unscoped_dedupes_and_normalises():
    spec = {"model_regex": r"gpt-\d+(?:\.\d+)?-(?:astra|sol|luna)"}
    assert lineup.parse("gpt-6-astra gpt-6-astra GPT-6.1-sol", spec) == ["gpt-6-astra", "gpt-6-1-sol"]


def test_parse_exclude():
    spec = {"model_regex": r"grok-[a-z0-9.-]+", "exclude": ["grok-imagine"]}
    assert lineup.parse("grok-4.7 grok-imagine", spec) == ["grok-4-7"]


def test_flagship_rules():
    assert lineup.flagship(["a-1", "b-2"], {}) == "a-1"
    assert lineup.flagship(["a-1", "b-2"], {"flagship": "b-.*"}) == "b-2"
    assert lineup.flagship([], {}) is None


def test_compare_new_and_retired():
    assert lineup.compare(["x", "y"], ["y", "z"]) == (["x"], ["z"])


def test_match_model():
    ids = ["claude-opus-5-5", "claude-sonnet-5-5", "claude-fable-5-1"]
    assert lineup.match_model("Opus 5.5", ids) == "claude-opus-5-5"
    assert lineup.match_model("5.5", ids) is None
    assert lineup.match_model("fable", ids) == "claude-fable-5-1"
    assert lineup.match_model("claude-fable-5-1", ids) == "claude-fable-5-1"
