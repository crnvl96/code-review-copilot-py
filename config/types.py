from typing import TypedDict


class Schema(TypedDict):
    name: str
    port: str
    prompt: str
    temp: float
