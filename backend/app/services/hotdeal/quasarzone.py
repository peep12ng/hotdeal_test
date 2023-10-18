from .common import HotdealServiceObject
from ...repositories import HotdealRepository
from bs4 import BeautifulSoup
import re
from ...data import Source
import asyncio

class QuasarzoneService(HotdealServiceObject):

    _source = Source.quasarzone

    def update(self, repo: HotdealRepository):

        data = []

        # get page
        max_page = 1
        categories = ["PC/하드웨어", "노트북/모바일", "가전/TV"]
        urls = [f"https://quasarzone.com/bbs/qb_saleinfo?page={page}&category={category}" for category in categories for page in range(max_page, 0, -1)]

        pages = asyncio.run(self._client.get_many(urls))

        for p in pages:
            bs = BeautifulSoup(p, "html.parser")
            heads = bs.find("tbody").find_all("tr")

            for h in heads:
                d = self.get(h)
                self._update(d, repo)

        return data
    
    def get(self, head):
        d = {}

        code = re.search('views/(.+?)?category', head.select_one("a.subject-link").attrs["href"]).group(1)[:-1]
        code
        d["id"] = self._get_hotdeal_id(code)

        url = f"https://quasarzone.com/bbs/qb_saleinfo/views/{code}"
        d["source_link"] = url

        r = asyncio.run(self._client.get(url))
        bs = BeautifulSoup(r, "html.parser")
        d["title"] = bs.find("title").text.split(" >")[0]

        table = bs.select_one("table.market-info-view-table")
        trs = table.find_all("tr")

        d["first_price"] = float(re.sub(r'[^0-9.]', '', trs[2].find("span").text))
        d["last_price"] = 0

        d["currency_type"] = trs[2].find("span").text.split("(")[1][:3]

        d["store_link"] = trs[0].find("a").text

        d["source_link"] = url

        if "종료" in bs.select_one("h1.title").text:
            d["is_done"] = True
        else:
            d["is_done"] = False
        d["is_blind"] = False

        return d