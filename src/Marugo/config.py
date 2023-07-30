from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    username:str
    password:str
    hashtags:list


def get_credentials():
    return Config(
        username=os.getenv("USERNAME"),
        password=os.getenv("PASSWORD"),
        hashtags=os.getenv("HASHTAGS").split(",")
    )
