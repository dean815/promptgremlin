"""Whole-plugin hygiene checks. They live here, outside plugin/, so that no shipped script walks
the plugin folder (and reaches its icon file)."""
import re
import unicodedata
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[2] / "plugin"
IMAGES = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg")


def _plugin_files():
    """Every file the plugin ships: the folder holding .claude-plugin/plugin.json."""
    skip = {"__pycache__", ".pytest_cache"}
    return [p for p in PLUGIN.rglob("*") if p.is_file() and not skip & set(p.relative_to(PLUGIN).parts)]


def test_no_invisible_or_bidi_characters_anywhere_in_the_plugin():
    hits = []
    for p in _plugin_files():
        if p.suffix.lower() in IMAGES:
            continue
        text = p.read_text(encoding="utf-8")
        hits += [(p.name, hex(ord(ch))) for ch in set(text)
                 if unicodedata.category(ch) == "Cf" or ch in "\u2028\u2029"]
    assert hits == [], hits


def test_every_non_image_plugin_file_is_under_240_kib():
    """The directory's limit for a non-image file is 256 KiB; keep headroom for the daily
    scoreboard.json, which grows with the number of models."""
    big = [(p.name, p.stat().st_size) for p in _plugin_files()
           if p.suffix.lower() not in IMAGES and p.stat().st_size >= 240 * 1024]
    assert big == [], big


def test_no_shipped_script_names_an_image_or_font_file_or_walks_the_folder():
    """The directory holds a plugin whose code refers to, or could reach, an image or font file."""
    exts = re.compile(r"[.](png|jpe?g|gif|webp|svg|ico|ttf|otf|woff2?)\b|rglob|os[.]walk", re.I)
    hits = [p.name for p in _plugin_files() if p.suffix == ".py" and exts.search(p.read_text(encoding="utf-8"))]
    assert hits == [], hits
