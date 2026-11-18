# azure-rag-demo

A RAG assistant on Azure: a model deployed in Microsoft Foundry answers questions using only passages retrieved from Azure AI Search, and cites its sources.

## Status

- **Part 1, done:** calling a Foundry deployment with the OpenAI SDK and with LangChain, and handling the classic errors.
- **Part 2, in progress:** embeddings, an Azure AI Search index, and the RAG pipeline.

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in your endpoint, key and deployment name
```

## Part 1: basics

| Script | What it shows |
| --- | --- |
| `basics/hello_azure.py` | A chat call with `AzureOpenAI`: endpoint, `api_version`, deployment name, tokens, `finish_reason` |
| `basics/hello_langchain.py` | The same call with `AzureChatOpenAI`, a prompt template and an LCEL chain |
| `basics/errors_demo.py` | 401, 404, connection error and content filter, and which ones to retry |

```bash
python basics/hello_azure.py
```

## Azure equivalents of my usual stack

| What I use | Azure equivalent |
| --- | --- |
| Qdrant / Milvus | Azure AI Search |
| OpenAI API | Azure OpenAI (deployments in Foundry) |
| Self-hosted models on Ollama | Models from the Foundry catalog |
| Kubernetes, Argo CD | AKS, or Container Apps |
| Langfuse | Foundry tracing, Application Insights |
| Secrets in env files | Key Vault and managed identity |
