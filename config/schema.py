import os
from config import constants as c, types as t


class Config:
    def __init__(self):
        self._name = ""
        self._port = ""
        self._prompt = ""
        self._temp = ""

    def load(self):
        self._name = os.getenv(c.AI_MODEL_NAME, "")
        self._port = os.getenv(c.AI_MODEL_PORT, "")
        self._prompt = os.getenv(c.AI_MODEL_PROMPT, "")
        self._temp = os.getenv(c.AI_MODEL_TEMPERATURE, "")

        return self

    def validate(self):
        if self._name == "":
            raise ValueError(f"You must provide a value for {c.AI_MODEL_NAME}")

        if self._port == "":
            raise ValueError(f"You must provide a value for {c.AI_MODEL_PORT}")

        if self._prompt == "":
            raise ValueError(f"You must provide a value for {c.AI_MODEL_PROMPT}")

        if self._temp == "":
            raise ValueError(f"You must provide a value for {c.AI_MODEL_TEMPERATURE}")

        return self

    def parse(self) -> t.Schema:
        temp = float(self._temp)

        return {
            "name": self._name,
            "port": self._port,
            "prompt": self._prompt,
            "temp": temp,
        }
