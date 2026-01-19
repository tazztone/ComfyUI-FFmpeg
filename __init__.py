from .nodes_map import NODE_CLASS_MAPPINGS_V3
from comfy_api.latest import ComfyExtension, io

WEB_DIRECTORY = "js"


class FFmpegExtension(ComfyExtension):
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return NODE_CLASS_MAPPINGS_V3


async def comfy_entrypoint() -> FFmpegExtension:
    return FFmpegExtension()


__all__ = [
    "WEB_DIRECTORY",
    "comfy_entrypoint",
]
