### "ffmpeg" module for disc-pack-creator

from pathlib import Path
from subprocess import run
from os import remove as rmfile
from modules._ensureffmpeg import ensureffmpeg

FFMPEGPATH = ensureffmpeg()

def _ffrun(*args: str) -> None:
    """
    Runs ffmpeg with the given arguments
    """
    run(
        (FFMPEGPATH, *args),
        capture_output=True,
        check=True,
    )

class FFmpeg:
    """
    Class containing wrappers for various FFmpeg commands
    """

    def to_ogg(file: Path) -> None:
        """
        Converts any file to a .ogg file and removes the original file
        """
        _ffrun("-i", file, file.with_suffix(".ogg"))
        rmfile(file)

    def to_mono(file: Path) -> None:
        """
        Converts a stereo audio file to mono
        """
        ...