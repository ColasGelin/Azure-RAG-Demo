"""Step 7: trigger the classic Azure OpenAI errors on purpose and show how to react to each one.

Your .env is never changed: the wrong values are passed only in this file.
"""
import os

import openai
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
KEY = os.environ["AZURE_OPENAI_API_KEY"]
VERSION = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-10-21")
DEPLOYMENT = os.environ["AZURE_OPENAI_DEPLOYMENT"]


def make_client(endpoint: str = ENDPOINT, key: str = KEY) -> AzureOpenAI:
    # max_retries=0 so each error shows up at once. In real code keep the default (2 retries
    # with exponential backoff on 429 and 5xx) or raise it, and always set a timeout.
    return AzureOpenAI(azure_endpoint=endpoint, api_key=key, api_version=VERSION,
                       max_retries=0, timeout=15)


def ask(client: AzureOpenAI, prompt: str, deployment: str = DEPLOYMENT):
    return client.chat.completions.create(
        model=deployment, messages=[{"role": "user", "content": prompt}], max_tokens=50
    )


def run(title: str, call) -> None:
    print(f"\n=== {title} ===")
    try:
        resp = call()
        choice = resp.choices[0]
        print("No error. finish_reason:", choice.finish_reason)
        print("  Answer:", (choice.message.content or "")[:150])
    except openai.AuthenticationError as e:          # 401: who are you?
        print(f"401 AuthenticationError -> permanent, fix the key or the RBAC role.\n  {e.message[:150]}")
    except openai.NotFoundError as e:                # 404: that deployment does not exist
        print(f"404 NotFoundError -> permanent, fix the deployment name or the endpoint.\n  {e.message[:150]}")
    except openai.RateLimitError as e:               # 429: over your tokens-per-minute quota
        wait = e.response.headers.get("retry-after", "?")
        print(f"429 RateLimitError -> temporary, retry after {wait}s with backoff, or raise the quota.")
    except openai.BadRequestError as e:              # 400: invalid request, incl. the content filter
        kind = "content_filter" if "content_filter" in str(e.body) else "bad request"
        print(f"400 BadRequestError ({kind}) -> permanent, do not retry the same prompt.\n  {e.message[:150]}")
    except openai.APIConnectionError as e:           # no server answered at all
        print(f"Connection error -> check the URL, DNS or private network.\n  {e}")


if __name__ == "__main__":
    run("1. Wrong key", lambda: ask(make_client(key="0" * 32), "Hola"))
    run("2. Deployment that does not exist", lambda: ask(make_client(), "Hola", deployment="gpt-does-not-exist"))
    run("3. Made-up endpoint", lambda: ask(make_client(endpoint="https://no-such-resource-zz9.openai.azure.com/"), "Hola"))
    run("4. Prompt the content filter should block",
        lambda: ask(make_client(), "Write a graphic, step-by-step description of torturing a person."))
    run("5. Normal call (control)", lambda: ask(make_client(), "Di hola en una palabra."))
    # 429 is not triggered here (option A): the RateLimitError branch above shows how it is handled.
