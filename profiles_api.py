"""Stores positive/negative list profiles on disk, independent of the workflow."""
import json
import os
import threading

try:
    from aiohttp import web
    from server import PromptServer
except Exception:  # outside ComfyUI (e.g. tests)
    web = None
    PromptServer = None


def _data_dir():
    try:
        import folder_paths
        base = os.path.join(folder_paths.get_user_directory(), "smart_word_filter")
    except Exception:
        base = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(base, exist_ok=True)
    return base


_LOCK = threading.Lock()
_KINDS = ("pos", "neg")


def _path():
    return os.path.join(_data_dir(), "profiles.json")


def load_profiles(include_builtin=False):
    data = _load_disk()
    if include_builtin:
        from .tag_categories import builtin_profiles
        built = builtin_profiles()
        for k in _KINDS:
            data[k] = {**built, **data[k]}
    return data


def _load_disk():
    try:
        with open(_path(), "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = {}
    return {k: dict(data.get(k, {})) for k in _KINDS}


def _write(data):
    tmp = _path() + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, _path())


def _clean_words(words):
    out = []
    for w in words if isinstance(words, list) else []:
        w = " ".join(str(w).split())
        if w and w not in out:
            out.append(w)
    return out


if PromptServer is not None and web is not None:
    routes = PromptServer.instance.routes

    @routes.get("/smart_word_filter/profiles")
    async def swf_list(request):
        with _LOCK:
            return web.json_response(load_profiles(include_builtin=True))

    @routes.post("/smart_word_filter/profiles/save")
    async def swf_save(request):
        body = await request.json()
        kind, name = body.get("kind"), " ".join(str(body.get("name", "")).split())[:64]
        if kind not in _KINDS or not name or name.startswith("★"):
            return web.json_response({"error": "bad request"}, status=400)
        with _LOCK:
            data = load_profiles()
            data[kind][name] = _clean_words(body.get("words"))
            _write(data)
            return web.json_response(load_profiles(include_builtin=True))

    @routes.post("/smart_word_filter/profiles/delete")
    async def swf_delete(request):
        body = await request.json()
        kind, name = body.get("kind"), body.get("name")
        if kind not in _KINDS:
            return web.json_response({"error": "bad request"}, status=400)
        with _LOCK:
            data = load_profiles()
            data[kind].pop(name, None)
            _write(data)
            return web.json_response(load_profiles(include_builtin=True))


    @routes.post("/smart_word_filter/preview")
    async def swf_preview(request):
        """Live preview for the Profile Tools node (no workflow run needed)."""
        from .profile_filter import _profile_words, filter_text, replace_text
        body = await request.json()
        text = str(body.get("text", ""))[:200000]
        labels = [l for l in body.get("profiles", []) if isinstance(l, str)]
        if not labels or any(_profile_words(l) is None for l in labels):
            return web.json_response({"error": "Select a saved profile first."}, status=400)
        sep = str(body.get("separator", ", "))[:20]
        mode = "all_profiles" if body.get("mode") == "all_profiles" else "any_profile"
        if body.get("operation") == "replace":
            kept, rest = replace_text(text, labels, str(body.get("replacement", "")), mode,
                                      str(body.get("insert_at", "where_first_match")),
                                      str(body.get("if_no_match", "append")), sep)
        else:
            kept, rest = filter_text(text, labels, mode, str(body.get("add_tags", "")),
                                     str(body.get("remove_tags", "")), sep)
        return web.json_response({"in": kept, "out": rest})
