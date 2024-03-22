from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Dict, Tuple

from pathlib import Path
import re
import json
import logging
import os

logging.basicConfig()

__all__ = ("Check", )

class Check():
    def __init__(self) -> None:

        self.logger = logging.getLogger(__name__)

        self.__filepath = Path(os.getcwd(), "config.json")

        self.json = self.__get_json()


    def __get_json(self):
        try:
            with open(self.__filepath, "r") as f:
                s = json.loads(f.read())
                f.close()

                return s
            
        except FileNotFoundError:
            self.logger.error("config.json was not found! Please create it in the root folder.")
    
    def __save(self):
        with open(self.__filepath, "w") as f:
            f.write(json.dumps(self.json, indent=0))
            f.close()
    
    def __extract(self, url: str):
        return re.findall(r"watch\?v=(.*)", url)[0]

    def check(self, url: str):
        id = self.__extract(url)

        if id in self.json["UploadedIDs"]:
            return True
        
        self.json["UploadedIDs"].append(id)

        self.__save()

        return False