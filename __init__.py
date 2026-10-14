from . import profiles_api  # noqa: F401  (registers the API routes)
from .word_filter import NODE_CLASS_MAPPINGS as _M1, NODE_DISPLAY_NAME_MAPPINGS as _D1
from .profile_filter import NODE_CLASS_MAPPINGS as _M2, NODE_DISPLAY_NAME_MAPPINGS as _D2

NODE_CLASS_MAPPINGS = {**_M1, **_M2}
NODE_DISPLAY_NAME_MAPPINGS = {**_D1, **_D2}
WEB_DIRECTORY = "./js"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
