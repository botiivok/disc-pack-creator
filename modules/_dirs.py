### "_dirs" submodule for disc-pack-creator

from pathlib import Path

class Dirs:

    ROOT = Path(__file__).parent.parent

    FFMPEGDIR = ROOT / "ffmpeg"
    TEMP = ROOT / "temp"