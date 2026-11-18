"""Step 6: the same call through LangChain, with a prompt template and a chain."""
import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI

load_dotenv()

# Same 3 Azure settings as hello_azure.py, plus the deployment.
llm = AzureChatOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-10-21"),
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    max_tokens=200,
)

# A reusable prompt with a variable: in part 2, {question} gets a {context} next to it.
prompt = ChatPromptTemplate.from_messages([
    ("system", "Responde en español, en una sola frase."),
    ("user", "{question}"),
])

# A chain: prompt -> model -> plain text. The | pipes each step's output into the next.
chain = prompt | llm | StrOutputParser()

print(chain.invoke({"question": "¿Qué es Azure AI Search?"}))

# The raw message still carries the metadata: tokens and finish reason.
msg = (prompt | llm).invoke({"question": "¿Qué es una managed identity?"})
print(msg.content)
print("Tokens:", msg.usage_metadata)
print("Finish reason:", msg.response_metadata.get("finish_reason"))
