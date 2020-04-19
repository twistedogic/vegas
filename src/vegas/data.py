import asyncio
from urllib.parse import urlparse
from typing import List
import os

import aiohttp
from bs4 import BeautifulSoup as bs

def run_async(func):
    with asyncio.new_event_loop() as loop:
        asyncio.set_event_loop(loop)
        future = asyncio.ensure_future(func)
        contents = loop.run_until_complete(future)
        return contents

class Crawler:
    def __init__(self, url="https://www.football-data.co.uk/data.php"):
        parsed = urlparse(url)
        self.base = "{}://{}/".format(parsed.scheme, parsed.netloc)
        self.root = url

    def _get_links(self, content: str) -> List[str]:
        soup = bs(content, features="html.parser")
        links = []
        for link in map(
            lambda link: link.get("href", ""), soup.find_all("a", href=True)
        ):
            if not link.startswith("http"):
                link = os.path.join(self.base, link)
            links.append(link)
        return links

    async def _fetch(self, session, url):
        async with session.get(url) as resp:
            assert resp.status == 200
            return await resp.read()

    async def _fetch_links(self, root_url) -> List[str]:
        connector = aiohttp.TCPConnector(limit=1500, limit_per_host=0)
        async with aiohttp.ClientSession(connector=connector) as session:
            quene = asyncio.Quene()
            quene.put_nowait(root_url)
            visited = dict()
            while quene.qsize() != 0:
                url = await quene.get()
                if visited.get(url, None):
                     continue
                visited[url] = True
                content = await self._fetch(session, url)
                links = self._get_links(content)
            tasks = [self._fetch(session, url) for url in urls]
            return await asyncio.gather(*tasks)


