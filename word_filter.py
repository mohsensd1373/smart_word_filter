import json
import re

DEFAULT_RULES = json.dumps({"pos": [], "neg": [], "seen": []}, ensure_ascii=False)
SPLIT_RE = re.compile(r"[,\u060c\n]+")  # tag separator: comma (Latin / Arabic) or newline


def _norm(s):
    return " ".join(str(s).lower().split())


def canon(s):
    """Tag comparison: case, spaces and _ are equivalent (looking_at_viewer == looking at viewer)."""
    return _norm(s).replace("_", " ")


def tag_key(seg):
    """Tag key: without outer brackets and weights like (x:1.2)."""
    s, prev = seg.strip(), None
    while s != prev:
        prev = s
        s = re.sub(r"^[\(\[\{<]+|[\)\]\}>]+$", "", s).strip()
        s = re.sub(r":\s*-?[\d.]+$", "", s).strip()
    return _norm(s)


def extract_words(text):
    """Unique tags of the text in order of appearance."""
    out = []
    for seg in SPLIT_RE.split(text or ""):
        k = tag_key(seg)
        if k and canon(k) not in [canon(x) for x in out]:
            out.append(k)
    return out


def _parse_rules(raw):
    try:
        data = json.loads(raw) if raw else {}
    except Exception:
        data = {}
    def uniq(items):
        out, seen = [], set()
        for t in items:
            t = _norm(t)
            if t and canon(t) not in seen:
                seen.add(canon(t))
                out.append(t)
        return out

    neg = uniq(data.get("neg", []))
    neg_c = {canon(t) for t in neg}
    pos = [t for t in uniq(data.get("pos", [])) if canon(t) not in neg_c]  # negative wins
    return pos, neg


class SmartWordFilter:
    CATEGORY = "utils/text"
    FUNCTION = "run"
    OUTPUT_NODE = True
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("filtered_positive", "negative_words")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
                "filter_mode": (["remove_negatives", "only_positives"],),
                "negative_output": (["all_in_list", "found_in_text"],),
                "append_missing_positives": ("BOOLEAN", {"default": False}),
                "separator": ("STRING", {"default": ", "}),
                "rules": ("STRING", {"default": DEFAULT_RULES, "multiline": False}),
            }
        }

    def run(self, text, filter_mode, negative_output,
            append_missing_positives, separator, rules):
        pos, neg = _parse_rules(rules)
        pos_set, neg_set = {canon(p) for p in pos}, {canon(n) for n in neg}

        kept, pos_kept, pos_found, neg_found = [], [], [], []
        for seg in SPLIT_RE.split(text or ""):
            seg = seg.strip()
            k = tag_key(seg)
            if not seg or not k:
                continue
            c = canon(k)
            if c in neg_set:
                if k not in neg_found:
                    neg_found.append(k)
                continue
            kept.append(seg)
            if c in pos_set:
                pos_kept.append(seg)
                if c not in pos_found:
                    pos_found.append(c)

        out1_parts = pos_kept if filter_mode == "only_positives" else kept
        out1_parts = list(out1_parts)
        if append_missing_positives:
            out1_parts += [p for p in pos if canon(p) not in pos_found]
        out1 = separator.join(out1_parts)
        out2 = separator.join(neg if negative_output == "all_in_list" else neg_found)

        return {"ui": {"words": extract_words(text)}, "result": (out1, out2)}


NODE_CLASS_MAPPINGS = {"SmartWordFilter": SmartWordFilter}
NODE_DISPLAY_NAME_MAPPINGS = {"SmartWordFilter": "Smart Word Filter (Pos/Neg)"}
