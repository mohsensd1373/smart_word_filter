"""Folder-driven tag profiles.

The built-in (★) profiles are NOT hard-coded any more: they are generated from
the *.txt files inside tag_lists_default/ (shipped defaults) and the editable
copy tag_lists/. Each file (e.g. face.txt) becomes one profile (★ Face) whose
words are the lines of that file. Drop a new file like animals.txt in the
folder and a new ★ Animals profile appears automatically. Edits to the files are
picked up live (no ComfyUI restart needed). Files whose name starts with "_"
(e.g. _unsorted.txt, _version.txt) are ignored.
"""
import os
import re

from .tag_defaults import EXPLICIT

SPLIT_RE = re.compile(r"[,\u060c\n]+")  # comma (Latin / Arabic) or newline


def canon(s):
    return " ".join(str(s).lower().replace("_", " ").split())


LISTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tag_lists")
DEFAULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tag_lists_default")

# preferred display order for the well-known categories; extras are appended A-Z
PREFERRED_ORDER = ["subject", "face", "hair", "body", "pose", "clothing",
                   "objects", "background", "lighting", "camera_style"]

BUILTIN_PREFIX = "\u2605 "  # "★ "
LISTS_VERSION = "4"         # bump when the shipped defaults change

_HEADER = (
    "# Tag list for the '{cat}' profile.\n"
    "# One tag per line (or several separated by commas). Lines starting with # are comments.\n"
    "# Case and space/underscore differences are ignored. Changes apply live, no restart needed.\n"
    "# The profile name comes from THIS file name; adding a new <name>.txt file in\n"
    "# tag_lists/ or tag_lists_default/ creates a new '★ <Name>' profile automatically.\n"
)

_state = {"sig": None, "cats": [], "words": {}, "synced": False}


def _scan_category_files():
    cats = set()
    for d in (DEFAULTS_DIR, LISTS_DIR):
        if os.path.isdir(d):
            for fn in os.listdir(d):
                if fn.lower().endswith(".txt") and not fn.startswith("_"):
                    cats.add(fn[:-4])
    return cats


def discover_categories():
    """Category names discovered on disk, ordered by PREFERRED_ORDER then A-Z."""
    found = _scan_category_files()
    ordered = [c for c in PREFERRED_ORDER if c in found]
    extra = sorted(c for c in found if c not in PREFERRED_ORDER)
    return (ordered + extra) or list(PREFERRED_ORDER)


def _list_path(cat):
    return os.path.join(LISTS_DIR, cat + ".txt")


def _read_file(path):
    out = []
    with open(path, "r", encoding="utf-8-sig") as f:
        for line in f:
            if line.strip().startswith("#"):
                continue
            for t in SPLIT_RE.split(line):
                c = canon(t)
                if c and c not in out:
                    out.append(c)
    return out


def _default_words(cat):
    p = os.path.join(DEFAULTS_DIR, cat + ".txt")
    if os.path.exists(p):
        return _read_file(p)
    return [canon(w) for w in EXPLICIT.get(cat, [])]


def _ensure_files():
    os.makedirs(LISTS_DIR, exist_ok=True)
    cats = discover_categories()
    for cat in cats:
        p = _list_path(cat)
        if not os.path.exists(p):
            with open(p, "w", encoding="utf-8") as f:
                f.write(_HEADER.format(cat=cat) + "\n".join(_default_words(cat)) + "\n")
    if _state.get("synced"):
        return
    _state["synced"] = True
    vfile = os.path.join(LISTS_DIR, "_version.txt")
    cur = None
    if os.path.exists(vfile):
        with open(vfile, "r", encoding="utf-8") as f:
            cur = f.read().strip()
    if cur != LISTS_VERSION:
        known = set()
        for cat in cats:
            known |= set(_read_file(_list_path(cat)))
        for cat in cats:
            new = [w for w in _default_words(cat) if w not in known]
            if new:
                with open(_list_path(cat), "a", encoding="utf-8") as f:
                    f.write(f"\n# added by update v{LISTS_VERSION}\n" + "\n".join(new) + "\n")
                known |= set(new)
        with open(vfile, "w", encoding="utf-8") as f:
            f.write(LISTS_VERSION + "\n")


def signature():
    """Changes whenever any list file is added, removed or edited (live refresh)."""
    _ensure_files()
    parts = []
    for d in (DEFAULTS_DIR, LISTS_DIR):
        if os.path.isdir(d):
            for fn in sorted(os.listdir(d)):
                if fn.lower().endswith(".txt") and not fn.startswith("_"):
                    st = os.stat(os.path.join(d, fn))
                    parts.append(f"{fn}:{st.st_mtime_ns}:{st.st_size}")
    return "|".join(parts)


def refresh():
    """Re-read the list files if anything changed on disk."""
    sig = signature()
    if sig == _state["sig"]:
        return
    cats = discover_categories()
    words = {}
    for cat in cats:
        try:
            words[cat] = _read_file(_list_path(cat))
        except Exception as e:
            print(f"[SmartWordFilter] cannot read {cat}.txt: {e}")
            words[cat] = _default_words(cat)
    _state.update(sig=sig, cats=cats, words=words)


def _nice(cat):
    return cat.replace("_", " ").title()


def builtin_profiles():
    """{display_name: [words]} generated from the folder, e.g. '★ Face': [...]."""
    refresh()
    return {BUILTIN_PREFIX + _nice(c): list(_state["words"].get(c, [])) for c in _state["cats"]}


def builtin_words(name):
    return builtin_profiles().get(name)


def preset_match(name, tag):
    words = builtin_words(name)
    if words is None:
        return False
    return canon(tag) in {canon(w) for w in words}
