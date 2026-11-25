### "_ensureffmpeg" submodule for disc-pack-creator

from os import remove as rmfile, rename as movefile
from sys import platform
from zipfile import ZipFile
from tarfile import TarFile
from pathlib import Path
from subprocess import run
from enum import Enum
from httpx import Client
from modules._dirs import Dir

iswindows = platform == "win32"

FFMPEGURL = "https://github.com/FFmpeg-Builds/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest"

FFMPEGURL_WIN32 = f"{FFMPEGURL}-win64-lgpl.zip"
FFMPEGURL_LINUX = f"{FFMPEGURL}-linux64-lgpl.tar.xz"

class FfmpegState(Enum):
    NOT_INSTALLED = 0
    INSTALLED_LOCALLY = 1
    INSTALLED_ON_PATH = 2

client = Client(follow_redirects=True)

def _install_base(url: str, archive: type[ZipFile]|type[TarFile]) -> None:
    """
    Platform-independent function for installing & unpacking archives
    """
    response = client.get(url)
    ext = "".join(Path(url).suffixes)
    file = Dir.TEMP / f"ffmpeg-latest{ext}"
    unpackdir = Path(url).with_suffix("").name

    with open(file, "wb") as f:
        f.write(response.content)
    archive(file).extractall(Dir.TEMP)
    rmfile(file)
    
    movefile(Dir.TEMP / unpackdir, Dir.FFMPEGDIR)

def installffmpeg() -> None:
    """
    Installs FFmpeg locally at the project root
    """
    if iswindows:
        _install_base(FFMPEGURL_WIN32, ZipFile)
    else:
        _install_base(FFMPEGURL_LINUX, TarFile)

def checkffmpeg() -> int:
    """
    Checks if, and where FFmpeg is installed
    """
    if run(("ffmpeg",), capture_output=True).returncode == 0:
        return FfmpegState.INSTALLED_ON_PATH
    if Dir.FFMPEGDIR.exists():
        return FfmpegState.INSTALLED_LOCALLY
    return FfmpegState.NOT_INSTALLED

def ensureffmpeg() -> str|Path:
    """
    Checks if FFmpeg is installed, and installs it if not\n
    Returns the corresponding command
    """
    check = checkffmpeg()
    if check is FfmpegState.INSTALLED_ON_PATH:
        return "ffmpeg"
    if check is FfmpegState.NOT_INSTALLED:
        installffmpeg()
    return Dir.FFMPEGDIR / "bin" / ("ffmpeg.exe" if iswindows else "ffmpeg")