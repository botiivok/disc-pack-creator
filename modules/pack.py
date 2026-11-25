### "pack" module for disc-pack-creator

from uuid import uuid4
from typing import Self
from zipfile import ZipFile
from os import makedirs
from shutil import copyfile, rmtree
from pathlib import Path
from json import load as loadjson, dump as dumpjson
from _dirs import Dir

with open(Dir.ASSETS / "discs.json") as f: DISCS = loadjson(f)
with open(Dir.ASSETS / "formats.json") as f: FORMATS = loadjson(f)
TEMPLATEFILE = Dir.ASSETS / "pack-template.json"

class ResourcePack:

    def __init__(self) -> None:
        self.id = f"{uuid4()}"
        self.path = Dir.TEMP / self.id
        self.textures_dir = self.path / "assets" / "minecraft" / "textures" / "item"
        self.music_dir = self.path / "assets" / "minecraft" / "sounds" / "records"
        self.lang_dir = self.path / "assets" / "minecraft" / "lang"
        self.discs = set()

    def __enter__(self) -> Self:
        makedirs(self.textures_dir)
        makedirs(self.music_dir)
        makedirs(self.lang_dir)
        return self

    def __exit__(self, *_) -> None:
        with ZipFile(self.path.with_suffix(".zip"), "w") as zf:
            for dirname, _, files in self.path.walk():
                for file in files:
                    zf.write(dirname / file, dirname.relative_to(self.path) / file)
        rmtree(self.path)

    def latest_disc(self) -> str:
        maxformat, maxdisc = 0, None
        for disc in self.discs:
            if DISCS[disc]["format"] > maxformat:
                maxdisc = disc
        return maxdisc

    def add_textures(self, assets: dict[str, Path]) -> None:
        for disc, file in assets.items():
            self.discs.add(disc)
            copyfile(file, self.textures_dir / f"music_disc_{disc}.png")

    def add_music(self, assets: dict[str, Path]) -> None:
        for disc, file in assets.items():
            self.discs.add(disc)
            copyfile(file, self.music_dir / f"{disc}.ogg")

    def add_lang(self, assets: dict[str, str], langs: list[str] = ["en_US"]) -> None:
        for lang in langs:
            with open(self.lang_dir / f"{lang}.json", "w") as f:
                dumpjson(assets, f)

    def pack(self, icon: Path) -> None:
        latest_disc = DISCS[self.latest_disc()]
        mcmeta = self.path / "pack.mcmeta"
        copyfile(TEMPLATEFILE, mcmeta)
        copyfile(icon, self / "pack.png")
        with open(mcmeta, "r+") as f:
            content = f.read()
            f.seek(0)
            f.write(content
                .replace("%s", FORMATS[str(latest_disc["format"])])
                .replace("\"%d\"", str(latest_disc["format"]))
            )
            f.truncate()