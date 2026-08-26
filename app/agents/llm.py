from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    model="openrouter/free",
    temperature=0,
    max_tokens=4096,
    timeout=60,       # fail fast instead of hanging forever if OpenRouter
                       # is slow/stuck -- this was causing background jobs
                       # to sit in "running" indefinitely with no error.
    max_retries=1,     # avoid long silent internal retry chains on 429s
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


if __name__ == "__main__":
    response = llm.invoke("Say hello in one sentence.")
    print("CONTENT:", repr(response.content))
    print("RESPONSE METADATA:", response.response_metadata)
    print("ADDITIONAL KWARGS:", response.additional_kwargs)
    print("USAGE METADATA:", getattr(response, "usage_metadata", None))