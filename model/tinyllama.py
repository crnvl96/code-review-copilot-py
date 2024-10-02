from abc import ABC, abstractmethod
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

from config.config import Config


LlmContainerBaseUrl = "http://localhost:"
Template = """{prompt}

Code:

```{lang}
{content}
```

"""


class OllamaModel(ABC):
    @abstractmethod
    def generateChain(self, content: str):
        pass


class TinyLlama(OllamaModel):
    def __init__(self, config: Config):
        self.config = config
        self.template = Template

        self.prompt = config.schema["prompt"]
        self.name = config.schema["name"]
        self.lang = config.schema["lang"]
        self.temp = config.schema["temp"]
        self.port = config.schema["port"]

    def generateChain(self, content: str):
        template = ChatPromptTemplate.from_template(self.template)
        model = OllamaLLM(model=self.name)
        chain = template | model

        print(
            chain.invoke({"prompt": self.prompt, "lang": self.lang, "content": content})
        )
