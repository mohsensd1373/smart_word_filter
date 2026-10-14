import hashlib

from .profiles_api import load_profiles
from .tag_categories import refresh, signature
from .word_filter import SPLIT_RE, canon, tag_key

NONE_LABEL = "(no profile saved)"
EMPTY = "(none)"  # for the optional slots


def _labels():
    data = load_profiles(include_builtin=True)
    out = []
    for kind in ("pos", "neg"):
        for name in sorted(data[kind], key=str.lower):
            out.append(f"{kind} | {name}")
    return out or [NONE_LABEL]


def _profile_words(label):
    if " | " not in label:
        return None
    kind, name = label.split(" | ", 1)
    return load_profiles(include_builtin=True).get(kind, {}).get(name)


def _matcher(label):
    """A function telling whether a tag belongs to this profile (exact word-list match)."""
    wanted = {canon(w) for w in (_profile_words(label) or [])}
    return lambda k: canon(k) in wanted


def _parse(text):
    """[(segment, key)] without empty items."""
    out = []
    for seg in SPLIT_RE.split(text or ""):
        seg = seg.strip()
        k = tag_key(seg)
        if seg and k:
            out.append((seg, k))
    return out


def filter_text(text, labels, mode="any_profile", add_tags="", remove_tags="", separator=", "):
    """split: keep tags of the selected profiles; add_tags forced in, remove_tags forced out.
    Returns (kept, rest).
    """
    refresh()
    matchers = [_matcher(l) for l in labels]
    combine = all if mode == "all_profiles" else any
    removed = {canon(k) for _, k in _parse(remove_tags)}
    adds, add_keys = [], set()
    for seg, k in _parse(add_tags):
        if canon(k) not in add_keys:
            add_keys.add(canon(k))
            adds.append((seg, k))

    inside, outside, inside_keys = [], [], set()
    for seg, k in _parse(text):
        c = canon(k)
        if c in removed:
            outside.append(seg)
        elif c in add_keys or (matchers and combine(m(k) for m in matchers)):
            inside.append(seg)
            inside_keys.add(c)
        else:
            outside.append(seg)
    for seg, k in adds:  # added tags that are not in the text are appended at the end
        c = canon(k)
        if c not in removed and c not in inside_keys:
            inside.append(seg)
            inside_keys.add(c)
    return separator.join(inside), separator.join(outside)


def replace_text(text, labels, replacement, mode="any_profile",
                 insert_at="where_first_match", if_no_match="append", separator=", "):
    """replace: remove the profile tags from the text and put the replacement tags in their place.
    Returns (result, removed_tags).
    """
    refresh()
    matchers = [_matcher(l) for l in labels]
    combine = all if mode == "all_profiles" else any

    segs = _parse(text)
    rep, rep_keys = [], set()
    for seg, k in _parse(replacement):
        if canon(k) not in rep_keys:
            rep_keys.add(canon(k))
            rep.append(seg)

    matched = [combine(m(k) for m in matchers) for _, k in segs] if matchers else [False] * len(segs)
    removed = [seg for (seg, _), m in zip(segs, matched) if m]
    found = any(matched)

    will_insert = bool(rep) and not (if_no_match == "skip" and not found)
    place = insert_at
    if not found and place == "where_first_match":
        place = "start" if if_no_match == "prepend" else "end"

    out, inserted = [], False
    if will_insert and place == "start":
        out += rep
        inserted = True
    for (seg, k), m in zip(segs, matched):
        if m:
            if will_insert and not inserted and place == "where_first_match":
                out += rep
                inserted = True
            continue
        if will_insert and canon(k) in rep_keys:
            continue  # a replacement tag that already appears elsewhere is dropped (no duplicates)
        out.append(seg)
    if will_insert and not inserted:
        out += rep

    if not will_insert and found is False and if_no_match == "skip":
        out = [seg for seg, _ in segs]
    return separator.join(out), separator.join(removed)


class ProfileWordFilter:
    """Profile Tools: one node that filters (split) or swaps (replace) tags by profile."""
    CATEGORY = "utils/text"
    FUNCTION = "run"
    DESCRIPTION = (
        "Profile Tools - split or replace tags using saved profiles.\n"
        "operation=split: output 1 = tags inside the profile(s), output 2 = the rest. "
        "In the node, each tag has + (force-keep / want) and - (force-remove / don't want).\n"
        "operation=replace: removes the profile tags and inserts your 'replacement' tags; "
        "output 1 = result text, output 2 = removed tags.\n"
        "mode: any_profile = tag in at least one selected profile; all_profiles = in every one.\n"
        "The (★) profiles are built automatically from the tag_lists folder and refresh live."
    )
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("kept", "rest")
    SLOTS = ("profile", "profile_2", "profile_3", "profile_4")

    @classmethod
    def INPUT_TYPES(cls):
        labels = _labels()
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
                "operation": (["split", "replace"], {
                    "tooltip": "split: keep profile tags in output 1, the rest in output 2.   |   "
                               "replace: remove profile tags and insert the 'replacement' tags."}),
                "profile": (labels,),
                "separator": ("STRING", {"default": ", "}),
                "mode": (["any_profile", "all_profiles"], {
                    "tooltip": "any_profile: tag is in at least one selected profile (union)   |   "
                               "all_profiles: tag is in every selected profile (intersection)"}),
            },
            "optional": {
                "profile_2": ([EMPTY] + labels, {"default": EMPTY}),
                "profile_3": ([EMPTY] + labels, {"default": EMPTY}),
                "profile_4": ([EMPTY] + labels, {"default": EMPTY}),
                "add_tags": ("STRING", {"multiline": True, "default": "", "tooltip":
                             "[split] 'want' list (+): these tags are forced into output 1 even if they are "
                             "not in the profile. Also editable with the + button on each tag."}),
                "remove_tags": ("STRING", {"multiline": True, "default": "", "tooltip":
                                "[split] 'don't want' list (-): these tags are forced out to output 2 even if "
                                "they are in the profile. 'don't want' wins over 'want'."}),
                "replacement": ("STRING", {"multiline": True, "default": "", "tooltip":
                                "[replace] replacement tags (comma separated). Empty = just remove."}),
                "insert_at": (["where_first_match", "start", "end"], {"tooltip":
                              "[replace] where_first_match: at the first removed tag's position | "
                              "start / end: beginning or end of the text"}),
                "if_no_match": (["append", "prepend", "skip"], {"tooltip":
                                "[replace] when no profile tag is in the text: append / prepend the "
                                "replacement, or skip (leave the text unchanged)"}),
            },
        }

    @classmethod
    def _selected(cls, kw):
        sel = []
        for s in cls.SLOTS:
            v = kw.get(s)
            if v and v != EMPTY and v not in sel:
                sel.append(v)
        return sel

    @classmethod
    def IS_CHANGED(cls, text, **kw):
        h = hashlib.md5()
        for label in cls._selected(kw):
            h.update(("\n".join(_profile_words(label) or []) + "|" + label).encode("utf-8"))
        for n in ("operation", "mode", "separator", "add_tags", "remove_tags",
                  "replacement", "insert_at", "if_no_match"):
            h.update(str(kw.get(n)).encode())
        h.update(signature().encode())
        return h.hexdigest()

    @classmethod
    def VALIDATE_INPUTS(cls, **kw):
        sel = cls._selected(kw)
        if not sel or any(_profile_words(l) is None for l in sel):
            return "Select a saved profile (create one in the Smart Word Filter node, then refresh ComfyUI)."
        return True

    def run(self, text, operation, profile, separator, mode="any_profile", **kw):
        labels = self._selected({"profile": profile, **kw})
        if operation == "replace":
            res = replace_text(text, labels, kw.get("replacement", ""), mode,
                               kw.get("insert_at", "where_first_match"),
                               kw.get("if_no_match", "append"), separator)
        else:
            res = filter_text(text, labels, mode, kw.get("add_tags", ""),
                              kw.get("remove_tags", ""), separator)
        # "text" is sent to the UI so the preview also works when the text comes from another node
        return {"ui": {"text": [text or ""]}, "result": res}


NODE_CLASS_MAPPINGS = {"ProfileWordFilter": ProfileWordFilter}
NODE_DISPLAY_NAME_MAPPINGS = {"ProfileWordFilter": "Profile Tools (Split / Replace by Profile)"}
