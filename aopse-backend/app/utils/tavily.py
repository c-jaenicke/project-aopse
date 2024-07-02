import asyncio

from tavily import TavilyClient

from app.config import ConfigSingleton


class TavilySearch:
    def __init__(self):
        self.config = ConfigSingleton.get_instance()
        self.client = TavilyClient(self.config.aopse.tools["tavily"].api_key)

    async def search(self, query: str):
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(
            None,
            self.client.search,
            query,
            "advanced"
        )
        return result
