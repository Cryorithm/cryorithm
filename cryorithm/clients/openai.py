import os
from openai import AsyncOpenAI as AsyncOpenAIClient
from llm_client import LLMClient


class OpenAIClientWrapper(LLMClient):
    def __init__(self, api_key: str = None):
        self.client = AsyncOpenAIClient(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    async def create_chat_completion_stream(
        self,
        model: str,
        messages: List[Dict[str, Any]],
    ) -> AsyncIterator:
        response_stream = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
        )
        async for chunk in response_stream:
            yield chunk.choices[0].delta.content if "delta" in chunk.choices[0] else ""
