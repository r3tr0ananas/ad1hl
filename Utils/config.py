from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Dict

import json
import logging

logging.basicConfig()

__all__ = ("Config", )

class Config:
    def __init__(self, file: str):
        self.user_data = self.__get_user_data(file)
        self.logger = logging.getLogger(__name__)
    
    def __get_json(self, file: str) -> Dict:
        try:
            with open(file, "r") as f:
                return json.loads(f.read())
        except FileNotFoundError:
            self.logger.error("config.json was not found! Please create it in the root folder.")

    def __get_user_data(self, file) -> str:
        js = self.__get_json(file)
        return js["user_profile"]