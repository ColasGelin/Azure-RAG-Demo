"""Step 5: call a model deployed in Microsoft Foundry with the OpenAI SDK."""
import os

from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()  # reads .env into os.environ

# The Azure client: same SDK as OpenAI, but it points at YOUR Azure resource.
client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],  # your resource's URL
    api_key=os.environ["AZURE_OPENAI_API_KEY"],          # in production: managed identity instead
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-10-21"),  # Azure versions its API by date
)

resp = client.chat.completions.create(
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],  # the DEPLOYMENT name, not "gpt-4o-mini"
    messages=[
        {"role": "system", "content": "Responde en español, en una sola frase."},
        {"role": "user", "content": "¿Qué es un RAG?"},
    ],
    max_tokens=200,
)

choice = resp.choices[0]
print("Answer:       ", choice.message.content)
print("Finish reason:", choice.finish_reason)  # stop | length | content_filter
print("Real model:   ", resp.model)            # the model behind your deployment
print("Tokens:        in", resp.usage.prompt_tokens, "/ out", resp.usage.completion_tokens)
