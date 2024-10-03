from abc import ABC, abstractmethod
from langchain_ollama import ChatOllama

from config.tinyllama_config import Config


LlmContainerBaseUrl = "http://localhost:"


class OllamaModel(ABC):
    @abstractmethod
    def generateChain(self, content: str):
        pass


class TinyLlama(OllamaModel):
    def __init__(self, config: Config):
        self.config = config
        self.name = config.schema["name"]
        self.temp = config.schema["temp"]
        self.port = config.schema["port"]

        self.prompt = config.schema["prompt"]  # not being actually used right now
        self.lang = config.schema["lang"]

    def generateChain(self, content: str):
        llm = ChatOllama(
            model=self.name,
            temperature=self.temp,
            base_url=f"{LlmContainerBaseUrl}{self.port}",
        )

        prompt = [
            (
                "system",
                f"You are a experienced programmer that explains snippets of code in {self.lang}. Explain the user code.",
            ),
            ("human", f"{content}"),
        ]

        res = llm.invoke(prompt)
        print(res.content)
