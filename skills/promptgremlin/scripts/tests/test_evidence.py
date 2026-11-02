"""evidence.json: every task type names metrics the data has, with weights that add up."""
import json
import re
from pathlib import Path

from pglib import livebench as L
from pglib import scoreboard as S

HERE = Path(__file__).resolve().parent
SKILL = HERE.parents[1]
EVIDENCE = json.loads((SKILL / "evidence.json").read_text(encoding="utf-8"))
BUNDLED = json.loads((SKILL / "scoreboard.json").read_text(encoding="utf-8"))
TYPES = sorted(p.stem for p in (SKILL / "types").glob("*.md"))
SUITES = {f"livebench:{x}" for x in L.SUITES}
# The slot flags guidance.py --suggest accepts, with a value each board has, for "name=*" slots.
SLOTS = {"run_length": "long", "language": "french", "style": "photorealistic", "input": "image"}


def _resolved():
    """(type, condition, resolved block) for each type's base and each of its slots."""
    for type_, block in EVIDENCE.items():
        yield type_, None, S.resolve_evidence(EVIDENCE, type_, {})
        for cond in block.get("slots", {}):
            name, _, want = cond.partition("=")
            yield type_, cond, S.resolve_evidence(EVIDENCE, type_, {name: SLOTS[name] if want == "*" else want})


def _keys(ev):
    return [k for part in ("main", "support") for k in ev.get(part, {})]


def test_every_type_has_evidence():
    assert sorted(EVIDENCE) == TYPES


def test_slot_flags_exist_in_guidance():
    src = (SKILL / "scripts" / "guidance.py").read_text(encoding="utf-8")
    for name in SLOTS:
        assert f'"--{name.replace("_", "-")}"' in src, name


def test_slots_name_known_slots():
    for type_, block in EVIDENCE.items():
        for cond, mod in block.get("slots", {}).items():
            name, eq, want = cond.partition("=")
            assert eq and want and name in SLOTS, (type_, cond)
            for part in mod.values():
                for key in (part if isinstance(part, dict) else {}):
                    for ph in re.findall(r"\{(\w+)\}", key):
                        # resolve_evidence fills only the slot's own placeholder, and only for "*".
                        assert ph == name and want == "*", (type_, cond, key)


def test_weights_sum_to_one():
    for type_, cond, ev in _resolved():
        assert ev.get("main"), (type_, cond)
        total = sum(ev.get("main", {}).values()) + sum(ev.get("support", {}).values())
        assert abs(total - 1.0) <= 0.01, (type_, cond, total)
        assert all(w > 0 for k in ("main", "support") for w in ev.get(k, {}).values()), (type_, cond)


def test_metrics_exist_in_the_data():
    """A mistyped key or cost suite would silently score every model as no data."""
    for type_, cond, ev in _resolved():
        for key in _keys(ev):
            assert "{" not in key, (type_, cond, key)
            if key.startswith("livebench:"):
                assert key in SUITES, (type_, cond, key)
            else:
                assert key in BUNDLED["boards"], (type_, cond, key)
        if "cost_suite" in ev:
            assert ev["cost_suite"] in SUITES, (type_, cond, ev["cost_suite"])


def test_media_types_use_arena_boards_only():
    """Image and video prices come in Phase 3; until then they have no cost suite."""
    for type_, cond, ev in _resolved():
        if type_ in ("image", "video"):
            assert all(k.startswith("lmarena:") for k in _keys(ev)), (type_, cond)
            assert "cost_suite" not in ev, (type_, cond)


def test_media_input_slots_use_the_edit_and_start_frame_boards():
    """The design's modifiers: editing an image (image_edit), a video from a start frame
    (image_to_video). Video editing has no board in the data yet."""
    main = lambda t, slots: S.main_key(S.resolve_evidence(EVIDENCE, t, slots))
    assert main("image", {"input": "image"}) == "lmarena:image_edit"
    assert main("image", {"input": "image", "style": "photorealistic"}) == "lmarena:image_edit"
    assert S.resolve_evidence(EVIDENCE, "image", {"input": "image", "style": "art"})["support"] == {}
    assert main("video", {"input": "image"}) == "lmarena:image_to_video"
    assert main("video", {}) == "lmarena:text_to_video"
