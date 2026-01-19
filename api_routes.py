from server import PromptServer
from aiohttp import web
import subprocess
import json
import os
import folder_paths

routes = PromptServer.instance.routes


def validate_path(path):
    if not path:
        return False

    # Normalize path to handle different OS separators
    path = os.path.abspath(path)

    # Get allowed directories
    input_dir = os.path.abspath(folder_paths.get_input_directory())
    output_dir = os.path.abspath(folder_paths.get_output_directory())
    temp_dir = os.path.abspath(folder_paths.get_temp_directory())

    # Check if path is within allowed directories
    allowed_dirs = [input_dir, output_dir, temp_dir]

    # Also check user configured extra model paths if relevant,
    # but for LosslessCut we primarily care about input/output videos.

    for safe_dir in allowed_dirs:
        if path.startswith(safe_dir):
            return True

    return False


@routes.post("/comfyui-ffmpeg/metadata")
async def get_video_metadata(request):
    try:
        data = await request.json()
        video_path = data.get("path")

        if not video_path:
            return web.json_response({"error": "No path provided"}, status=400)

        if not os.path.exists(video_path):
            return web.json_response({"error": "File not found"}, status=404)

        if not validate_path(video_path):
            return web.json_response(
                {"error": "Security violation: Path not allowed"}, status=403
            )

        # Run ffprobe
        cmd = [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=duration,r_frame_rate",
            "-show_entries",
            "packet=pts_time,flags",
            "-of",
            "json",
            video_path,
        ]

        # Run in a separate thread to avoid blocking the event loop
        # Since we are in an async function, subprocess.run would block.
        # But for simplicity in this initial port, we can use synchronous run if it's fast enough,
        # or better: use asyncio.create_subprocess_exec (but that requires parsing stdout async).
        # For now, let's stick to the existing logic but wrap it potentially?
        # Actually, let's keep it simple. ffprobe is usually fast for metadata,
        # BUT for keyframes on large files it might take time.
        # Ideally: await asyncio.to_thread(...)

        try:
            import asyncio

            process = await asyncio.create_subprocess_exec(
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                return web.json_response(
                    {"error": f"ffprobe failed: {stderr.decode()}"}, status=500
                )

            data = json.loads(stdout.decode())

        except Exception as e:
            return web.json_response(
                {"error": f"Execution error: {str(e)}"}, status=500
            )

        keyframes = []
        if "packets" in data:
            for packet in data.get("packets", []):
                if "K" in packet.get("flags", ""):
                    keyframes.append(float(packet["pts_time"]))

        if not data.get("streams"):
            return web.json_response({"error": "No video stream found"}, status=500)

        fps_str = data["streams"][0]["r_frame_rate"]
        num, den = map(int, fps_str.split("/"))
        fps = num / den if den != 0 else 0

        result = {
            "duration": float(data["streams"][0].get("duration", 0)),
            "fps": fps,
            "keyframes": keyframes,
        }

        return web.json_response(result)

    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)


@routes.get("/comfyui-ffmpeg/stream")
async def stream_video(request):
    video_path = request.query.get("path")

    if not video_path:
        return web.Response(status=400, text="Missing path")

    if not os.path.exists(video_path):
        return web.Response(status=404, text="File not found")

    if not validate_path(video_path):
        return web.Response(status=403, text="Security violation: Path not allowed")

    return web.FileResponse(video_path)
