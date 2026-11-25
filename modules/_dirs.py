### "_dirs" submodule for disc-pack-creator

from pathlib import Path

class Dir:
    """
    Class containing directories
    """

    ROOT = Path(__file__).parent.parent

    ASSETS = ROOT / "assets"
    FFMPEGDIR = ROOT / "ffmpeg"
    TEMP = ROOT / "temp"