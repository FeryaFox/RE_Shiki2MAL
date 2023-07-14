import requests
from bs4 import BeautifulSoup
import arrow
import re
import json
from .dataclass import Histories
from .utils import convert_dict_to_dataclass_history
from .exception import (ShikimoriEmptyHistory,
                        ShikimoriGetHistoryError,
                        ShikimoriProfileNotfound,
                        ShikimoriTooManyRequests,
                        ShikimoriForbidden)
from dataclasses import dataclass
import backoff

class ShikimoriHistoryGetter:
    @dataclass
    class __SoupInfo:
        soup: BeautifulSoup
        next_page: bool

    def __init__(
            self,
            username: str,
            headers = None
    ) -> None:
        if headers is not None:
            self.headers = headers
        else:
            self.headers = {
                'Accept': '*/*',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
                'Accept-Language': 'en-US;q=0.5,en;q=0.3',
                'Cache-Control': 'max-age=0',
                'DNT': '1',
                'Upgrade-Insecure-Requests': '1'
            }
        self.username = username

    def get_histories(
            self,
            page: int = 1
    ) -> Histories:
        return self.__fetch_and_parse_history(page)

    def get_all_histories(self) -> Histories:
        page = 1
        news = Histories([], False)
        next_page = True
        while next_page:
            # news_t, next_page = self.__fetch_and_parse_history(page)
            history = self.__fetch_and_parse_history(page)
            news.histories += history.histories
            if history.next_page:
                page += 1
                continue
            next_page = False
        return news

    def __fetch_and_parse_history(
            self,
            page: int = 1
    ) -> Histories:
        try:
            soup_info = self.__fetch_history(page)
        except ShikimoriEmptyHistory:
            return Histories([], False)
        history = self.__parse_history(soup_info.soup)
        r = []
        for i in history:
            if (c := convert_dict_to_dataclass_history(i)) is not None:
                r.append(c)
        return Histories(r, soup_info.next_page)

    @backoff.on_exception(
        backoff.expo,
        (
            ShikimoriTooManyRequests
        ),
        max_time=10,
        max_tries=20
    )
    def __fetch_history(
            self,
            page: int = 1
    ) -> __SoupInfo | None:
        r = requests.get(f"https://shikimori.me/{self.username}/history/logs/{page}.json", headers=self.headers)
        match r.status_code:
            # TODO откопать где-то ВСЕ коды
            case 200:
                pass
            case 403:
                raise ShikimoriForbidden()
            case 404:
                raise ShikimoriProfileNotfound(self.username)
            case 429:
                raise ShikimoriTooManyRequests()
            case _:
                raise ShikimoriGetHistoryError(self.username, r.status_code)

        r_json = r.json()
        next_page = False
        if "postloader" in r_json.keys():
            next_page = True
        if r_json["content"] is not None:
            soup = BeautifulSoup(r_json["content"], "html.parser")
            return self.__SoupInfo(soup, next_page)
        raise ShikimoriEmptyHistory()

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

    def __parse_history(
            self,
            news: BeautifulSoup
    ) -> list:
        r = news.find_all("div", {"class": "b-user_rate_log"})
        stories = []
        for i in r:
            stories.append(self.__parse_info_from_history(i))
        return stories
