import requests
import time
from abc import abstractmethod, abstractclassmethod
from ...data import Source
from injector import inject
from aiohttp import ClientSession
import asyncio

from ...repositories import HotdealRepository

class RequestError(RuntimeError):
    def __init__(self, message, code, url, response_headers: dict = None):
        self.message = message
        self.code = code
        self.url = url
        self.response_headers = response_headers

class ClientObject:
    async def get(self, url: str):
        async with ClientSession() as session:
            result = await asyncio.gather(self._get(session, url))

            return result[0]
        
    async def get_many(self, urls: list[str]):
        async with ClientSession() as session:
            results = await asyncio.gather(*[self._get(session, url) for url in urls])

            return results
    
    async def _get(self, session: ClientSession, url: str):
        async with session.get(url) as res:

            if res.status==429:
                await asyncio.sleep(10)
                print(429, url)
                return await self._get(session, url)
            elif res.status>=400:
                raise RequestError(res.reason, url, res.status, res.headers)
            
            content_type = res.headers.get("Content-Type", "application/octet-stream")

            if "APPLICATION/JSON" in content_type:
                data = await res.json()
            else:
                data = await res.text("utf-8")
            
            return data

class HotdealServiceObject():

    @inject
    def __init__(self,
                client: ClientObject):
        
        self._client = client
    
    @abstractmethod
    def update(self):
        pass

    def _update(self, d: dict, repo: HotdealRepository):
        hotdeal = repo.new(**d)

        if repo.exists(hotdeal.id):
            repo.update(hotdeal, ["is_blind", "is_done"])
        else:
            print("add")
            repo.add(hotdeal)
        
        print(f"update complete id{hotdeal.id}")

    @abstractmethod
    def get(self):
        pass
    
    @property
    @abstractmethod
    def _source(self) -> Source:
        pass

    def _get_hotdeal_id(self, code:str) -> str:
        return self._source.hotdeal_id_header + f"_{code}"