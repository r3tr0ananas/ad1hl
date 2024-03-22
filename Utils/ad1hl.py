from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Dict, Tuple

from yt_dlp import YoutubeDL
import os
from datetime import timedelta
import subprocess
from os import remove
from pathlib import Path
import logging

logging.basicConfig()

_default_description = """Thanks for Listening! Subscribe for More!

I do not own the Music used in this Video.
--------------------
All rights goes to their respectful owners or owner
Source: https://youtube.com/watch?v={}
--------------------
For a takedown mail me at takedown@ad1hl.xyz"""

__all__ = ("AD1HL", )

class   AD1HL():
    def __init__(self) -> None:
        self.opts = {
            'format': 'best',
            'ext': 'mp4',
            'outtmpl': 'in/%(id)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'prefer_ffmpeg': True
        }
        self.logger = logging.getLogger(__name__)

    def __make_timedelta(self, duration: int) -> str:
        return timedelta(seconds=duration)
    
    def __download(self, url: str) -> Dict:
        with YoutubeDL(self.opts) as dl:
            info = dl.extract_info(url, download=True)

            _d = {
                "id": info["id"],
                "title": info["title"],
                "file": f'{info["id"]}.mp4',
                "duration": info["duration"]
            }

            return _d
        
    
    def __loop(self, data) -> Tuple[bool, str | Exception]:
        file = data["file"]
        f_duration = data["duration"]

        duration = 0

        while duration < 3600:
            duration += f_duration
        
        delta = self.__make_timedelta(duration)

        try:
            sub = subprocess.Popen(
                [
                    "ffmpeg",
                    "-stream_loop",
                    "-1",
                    "-i",
                    f"in/{file}",  
                    "-c",
                    "copy",
                    "-ss",
                    "00:00:00",
                    "-to",
                    f"{delta}",
                    f"out/{file[:-4]}_1hour.mp4"
                ]
            )

            sub.wait()

            self.logger.info(f"Video: {file[:-4]} looped to {delta}")
            return (True, f"{file[:-4]}_1hour.mp4")
        
        except Exception as e:
            self.logger.error(f"{e} occurred while transcoding!")
            return (False, e)
    
    def __gen(self, title: str, id: str) -> Tuple[str, str]:
        return title + " | 1 Hour", _default_description.format(id)
    
    def delete_maked(self, _input: str, output: str) -> bool:
        try:
            remove(_input)
            remove(output)
            return True
        except Exception as e:
            self.logger.error(f"{e} occurred while removing files")
            return False

    def make(self, url: str) -> Dict:
        dl_dict = self.__download(url)
        loop_tuple = self.__loop(dl_dict)

        title, description = self.__gen(dl_dict["title"], dl_dict["id"])

        _d = {
            "title": title,
            "description": description,
            "path": Path(os.getcwd(), "out", loop_tuple[1])
        }

        self.logger.info("Make successful", exc_info=loop_tuple[1])

        return _d
