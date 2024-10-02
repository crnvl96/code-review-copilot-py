from abc import ABC, abstractmethod
import os
from typing import TypedDict


AI_MODEL_NAME = "AI_MODEL_NAME"
AI_MODEL_PROMPT = "AI_MODEL_PROMPT"
AI_MODEL_PORT = "AI_MODEL_PORT"
AI_MODEL_TEMPERATURE = "AI_MODEL_TEMPERATURE"
SOURCE_CODE_LANG = "SOURCE_CODE_LANG"


class Args(TypedDict):
    name: str
    port: str
    prompt: str
    temp: str
    lang: str


class Schema(TypedDict):
    name: str
    port: str
    prompt: str
    temp: float
    lang: str


class Config(ABC):
    @property
    @abstractmethod
    def schema(self) -> Schema:
        pass

    @abstractmethod
    def load(self) -> Args:
        pass

    @abstractmethod
    def validate(self, args: Args) -> Args:
        pass

    @abstractmethod
    def parse(self, args: Args) -> Schema:
        pass


class ModelConfig(Config):
    @property
    def schema(self) -> Schema:
        loaded_args = self.load()
        validated_args = self.validate(loaded_args)
        return self.parse(validated_args)

    def load(self) -> Args:
        return {
            "name": os.getenv(AI_MODEL_NAME, ""),
            "lang": os.getenv(SOURCE_CODE_LANG, ""),
            "port": os.getenv(AI_MODEL_PORT, ""),
            "prompt": os.getenv(AI_MODEL_PROMPT, ""),
            "temp": os.getenv(AI_MODEL_TEMPERATURE, ""),
        }

    def validate(self, args: Args) -> Args:
        name = args["name"]
        if name == "":
            raise ValueError(f"You must provide a value for {AI_MODEL_NAME}")

        port = args["port"]
        if port == "":
            raise ValueError(f"You must provide a value for {AI_MODEL_PORT}")

        prompt = args["prompt"]
        if prompt == "":
            raise ValueError(f"You must provide a value for {AI_MODEL_PROMPT}")

        lang = args["lang"]
        if lang == "":
            raise ValueError(f"You must provide a value for {SOURCE_CODE_LANG}")

        temp = args["temp"]
        if temp == "":
            raise ValueError(f"You must provide a value for {AI_MODEL_TEMPERATURE}")

        return {
            "name": name,
            "lang": lang,
            "port": port,
            "prompt": prompt,
            "temp": temp,
        }

    def parse(self, args: Args) -> Schema:

        return {
            "name": args["name"],
            "lang": args["lang"],
            "port": args["port"],
            "prompt": args["prompt"],
            "temp": float(args["temp"]),
        }
