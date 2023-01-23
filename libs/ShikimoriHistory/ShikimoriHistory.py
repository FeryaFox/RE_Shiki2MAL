import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import arrow
import re
import json


# TODO Дописать на Enum и Dataclass
class ShikimoriHistoryGetter:

    def __init__(self, username: str) -> None:
        self.username = username
        self.headers = Headers(headers=True).generate()

    def get_news(self, page: int = 1) -> None:
        soup = self.__fetch_history(page)
        history = self.__parse_history(soup)
        for i in history:
            ...
        # print(soup.prettify())
        with open("../../h.html", "w") as g:
            g.write(soup.prettify())

    def __fetch_history(self, page: int = 1) -> BeautifulSoup:
        r = requests.get(f"https://shikimori.one/{self.username}/history/logs/{page}.json", headers=self.headers)
        # TODO проверка на пустой лог {'content': None}

        r_json = r.json()
        if r_json["content"] is not None:
            soup = BeautifulSoup(r_json["content"], "html.parser")
            return soup
        else:
            raise Exception("log is clear")

    @staticmethod
    def __parse_info_from_history(news: BeautifulSoup) -> dict:
        spans = news.find_all("span")
        history_id = spans[0].find_all("a")[0].get_text()[1:]
        time = news.find("time").get_attribute_list("datetime")
        history_time = arrow.get(time[0])
        anime_id_r = spans[3].find("a").get_attribute_list("href")[0]
        anime_id = re.findall('\d+', anime_id_r)
        print(json.loads(news.find("code").get_text()))
        return {"history_id": history_id, "history_time": history_time, "anime_id": anime_id}

    def __parse_history(self, news: BeautifulSoup) -> list:
        r = news.find_all("div", {"class": "b-user_rate_log"})
        stories = []
        for i in r:
            stories.append(self.__parse_info_from_history(i))
        return stories
