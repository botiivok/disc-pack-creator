### "ffmpeg" module for disc-pack-creator

from subprocess import run
from pathlib import Path
from _ensureffmpeg import ensureffmpeg

FFMPEGURL = "https://github.com/FFmpeg-Builds/FFmpeg-Builds/releases/download/latest/"
FFMPEGDIR = Path(__file__).parent.parent / "ffmpeg"
FFMPEG = ensureffmpeg()

def to_ogg(file: str) -> None:
    run(
        (FFMPEG,),
        check=True
    )

print(FFMPEG)