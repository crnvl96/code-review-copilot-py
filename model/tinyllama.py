from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

template = """Question: {question}

Code:
```{lang}
{code}
```

Answer: Let's give a brief and quick explanation about the piece of code above."""

prompt = ChatPromptTemplate.from_template(template)

model = OllamaLLM(model="llama3.1")

chain = prompt | model

print(chain.invoke({"question": "What is LangChain?"}))
