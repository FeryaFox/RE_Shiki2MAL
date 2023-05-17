import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import arrow
import re
import json
from .ShikimoriHistoryDataclass import History
from .utils import convert_dict_to_dataclass
from typing import Tuple


class ShikimoriHistoryGetter:

    def __init__(self, username: str) -> None:
        self.username = username
        self.headers = Headers(headers=True).generate()

    def get_news(self, page: int = 1) -> Tuple[list[History], bool]:
        return self.__fetch_and_parse_history(page)

    def get_all_news(self) -> list[History]:
        page = 1
        news = []
        next_page = True
        while next_page:
            news_t, next_page = self.__fetch_and_parse_history(page)
            news = news + news_t
            if next_page:
                page += 1
        return news

    def __fetch_and_parse_history(self, page: int = 1) -> Tuple[list[History], bool]:
        soup, next_page = self.__fetch_history(page)
        if soup is None:
            return [], False
        history = self.__parse_history(soup)
        r = []
        for i in history:
            if (c := convert_dict_to_dataclass(i)) is not None:
                r.append(c)
        return r, next_page

    def __fetch_history(self, page: int = 1) -> Tuple[BeautifulSoup, bool] | None:
        r = requests.get(f"https://shikimori.one/{self.username}/history/logs/{page}.json", headers=self.headers)

        r_json = r.json()
        next_page = False
        if "postloader" in r_json.keys():
            next_page = True
        if r_json["content"] is not None:
            soup = BeautifulSoup(r_json["content"], "html.parser")
            return soup, next_page
        else:
            return None

    @staticmethod
    def __parse_info_from_history(news: BeautifulSoup) -> dict:

        spans = news.find_all("span")
        history_id = spans[0].find_all("a")[0].get_text()[1:]
        time = news.find("time").get_attribute_list("datetime")
        history_time = arrow.get(time[0])
        object_id_r = spans[3].find("a").get_attribute_list("href")[0]
        history_type = object_id_r.split("/")[1]
        match history_type:
            case "mangas":
                history_type = "manga"
            case "animes":
                history_type = "anime"
        object_id = re.findall('\d+', object_id_r)[0]
        # print(json.loads(news.find("code").get_text()))
        return {"history_type": history_type, "history_id": history_id, "history_time": history_time, "object_id": object_id} | json.loads(news.find("code").get_text())

    def __parse_history(self, news: BeautifulSoup) -> list:
        r = news.find_all("div", {"class": "b-user_rate_log"})
        stories = []
        for i in r:
            stories.append(self.__parse_info_from_history(i))
        return stories
