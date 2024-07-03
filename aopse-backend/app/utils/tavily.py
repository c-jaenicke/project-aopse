import asyncio

from tavily import TavilyClient

from app.config import ConfigSingleton


class TavilySearch:
    def __init__(self):
        self.config = ConfigSingleton.get_instance()
        self.client = TavilyClient(self.config.aopse.tools["tavily"].api_key)

    def search(self, query: str):
        try:
            result = self.client.search(query, "advanced")
            return result
        except Exception as e:
            return str(e)
