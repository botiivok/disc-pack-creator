### "_ensureffmpeg" submodule for disc-pack-creator

from logging import getLogger
from os import remove as rmfile, rename as movefile
from sys import platform
from zipfile import ZipFile
from tarfile import TarFile
from pathlib import Path
from httpx import Client
from _dirs import Dirs

log = getLogger("modules._ensureffmpeg")

FFMPEGURL = "https://github.com/FFmpeg-Builds/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-"

FFMPEGURL_WIN32 = FFMPEGURL + "win64-lgpl.zip"
FFMPEGURL_LINUX = FFMPEGURL + "linux64-lgpl.tar.xz"

client = Client(follow_redirects=True)

def _install_base(url: str, archive: type[ZipFile]|type[TarFile]) -> None:
    """
    Base platform-independent function for installing
    """
    response = client.get(url)
    ext = "".join(Path(url).suffixes)
    file = Dirs.TEMP / f"ffmpeg-latest{ext}"
    unpackdir = Path(url).with_suffix("").name

    with open(file, "wb") as f:
        f.write(response.content)
    
    archive(file).extractall(Dirs.TEMP)
    movefile(Dirs.TEMP / unpackdir, Dirs.FFMPEGDIR)

def installffmpeg() -> None:
    """
    Installs ffmpeg
    """
    if platform == "win32":
        _install_base(FFMPEGURL_WIN32, ZipFile)
    else:
        _install_base(FFMPEGURL_LINUX, TarFile)