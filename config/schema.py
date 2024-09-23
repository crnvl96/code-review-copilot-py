import os
from config import constants as c, types as t


class Config:
    def __init__(self):
        self._name = ""
        self._port = ""
        self._prompt = ""
        self._temp = ""

    @property
    def schema(self) -> t.Schema:
        schema = self._load()._validate()._parse()
        return schema

    def _load(self):
        self._name = os.getenv(c.AI_MODEL_NAME, "")
        self._port = os.getenv(c.AI_MODEL_PORT, "")
        self._prompt = os.getenv(c.AI_MODEL_PROMPT, "")
        self._temp = os.getenv(c.AI_MODEL_TEMPERATURE, "")

        return self

    def _validate(self):
        if self._name == "":
            raise ValueError(f"You must provide a value for {c.AI_MODEL_NAME}")

        if self._port == "":
            raise ValueError(f"You must provide a value for {c.AI_MODEL_PORT}")

        if self._prompt == "":
            raise ValueError(f"You must provide a value for {c.AI_MODEL_PROMPT}")

        if self._temp == "":
            raise ValueError(f"You must provide a value for {c.AI_MODEL_TEMPERATURE}")

        return self

    def _parse(self) -> t.Schema:
        temp = float(self._temp)

        return {
            "name": self._name,
            "port": self._port,
            "prompt": self._prompt,
            "temp": temp,
        }
