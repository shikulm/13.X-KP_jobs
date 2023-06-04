import json
import os
import requests
from abc import ABC, abstractmethod
from src.file_manager import FileManager


class ServiceApi(ABC):
    """ Абстрактный класс для работы с API по вакансиям"""
    __slots__ = ('_api_key', '_data', 'req', 'url', 'params')

    @property
    def api_key(self):
        """Возвращает ключ для доступа к API"""
        return self._api_key

    @api_key.setter
    def api_key(self, key):
        """По названию переменной среды окружения (key)
        получает ключ для доступа к API"""
        self._api_key = os.environ.get(key)

    # def __init__(self, keywords: str = None, pagefrom: int = 1, pageto: int = 1):
    def __init__(self, keywords: str = None, pagefrom: int = 1):
        """Получает данные из API по ключевым словам keywords
        со страницы pagefrom"""
        req = self.get_from_api(keywords, pagefrom)

    @abstractmethod
    def get_from_api(self, keywords: str = None, page: int = 1):
        """Считывает данные из API по ключевым словам"""
        pass

    def save_api_to_file(self, filename: str):
        """Сохраняет все полученные из api данные в файл"""
        self.get_file_manager(filename).bulk_insert(self._data)


    @staticmethod
    def get_file_manager(filename):
        """Возвращает объект класса FileManager для работы с файлом"""
        return FileManager(filename)


class HH(ServiceApi):
    """Класс для работы с HeadHunter"""
    api_key = "API_KEY_HH"

    def get_from_api(self, keywords: str = None, page: int = 0):
        self.url = "https://api.hh.ru/vacancies"
        self.params = {
            "text": keywords,
            "page": page
        }
        self.req = requests.get(self.url, params=self.params)
        self._data = self.req.json()["items"]
        return self.req


class SJ(ServiceApi):
    """Класс для работы с Super Job"""
    api_key = "API_KEY_SJ"

    def __init__(self, keywords: str = None, pagefrom: int = 1):
        super().__init__(keywords, pagefrom)
        self.req = None
        self._data = None

    def get_from_api(self, keywords: str = None, page: int = 1):
        self.url = "https://api.superjob.ru/2.0/vacancies/"
        self.params = {
            "keywords": keywords,
            "page": page
        }
        # self.api_key = "API_KEY_SJ"
        self.api_key = os.environ.get("API_KEY_SJ")
        headers = {"X-Api-App-Id": self.api_key}
        self.req = requests.get(self.url, headers=headers, params=self.params)
        self._data = self.req.json()["objects"]
        return self.req

# hh = HH("Программист", 0)
#
# vac = []
# for item in hh.get_from_api().json()["items"]:
#     dic_vac = {"title": item["name"],
#                "link": item["alternate_url"],
#                "description": item["snippet"]['requirement'],
#                "salary": item["salary"]["from"] if item.get("salary") else None,
#                "city": item["area"]["name"]}
#
#     vac.append(dic_vac)
#
# print(vac)
#
# sj = SJ("Программист", 1)
#
# vacsj = []
# for item in sj.get_from_api().json()["objects"]:
#     dic_vac = {"title": item["profession"],
#                "link": item["link"],
#                "description": item["candidat"],
#                "salary": item["payment_from"],
#                "city": item["town"]["title"]}
#
#     vacsj.append(dic_vac)
#
# print(vacsj)
#
#
# hh.save_to_file(os.path.join("data", "hh.json"))
# sj.save_to_file(os.path.join("data", "sj.json"))