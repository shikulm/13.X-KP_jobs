import json
import os
import requests
from abc import ABC, abstractmethod



class ServiceApi(ABC):
    """ Абстрактный класс для работы с API по вакансиям"""

    @classmethod
    @property
    def api_key(cls):
        """Возвращает ключ для доступа к API"""
        return cls.__api_key

    @classmethod
    @api_key.setter
    def api_key(cls, key):
        """По названию переменной среды окружения (key)
        получает ключ для доступа к API"""
        cls.__api_key = os.environ.get(key)

    def getAPI_KEY(self, key):
        """По названию переменных среды окружения (key)
        сохраняет ключ для доступа к API"""

    def __init__(self, keywords: str = None, pagefrom: int = 1, pageto: int = 1):
        """Получает данные из API по ключевым словам
        со страниц в диапазоне от pagefrom до pageto"""
        self.__api_key = None

    def printj(dict_to_print: dict) -> None:
        """Выводит словарь в json-подобном удобном формате с отступами"""
        print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))


    @abstractmethod
    def _getfromapi(self, keywords: str = None, page: int = 1):
        """Считывает данные из API по ключевым словам"""
        pass

    @abstractmethod
    def savetofile(self, filename: str):
        """Сохраняет считанныцю информацию в файл"""
        pass

    @abstractmethod
    def readfromfile(self, filename: str):
        """Читает данные из файла"""
        pass


class HH(ServiceApi):
    """Класс для работы с HeadHunter"""
    API_KEY = "API_KEY_HH"
    def _getfromapi(self, keywords: str = None, page: int = 0):
        self.url = "https://api.hh.ru/vacancies"
        self.params = {
            "text": keywords,
            "page": page
        }
        return requests.get(self.url, params=self.params)



class SJ(ServiceApi):
    """Класс для работы с Super Job"""
    api_key = "API_KEY_SJ"
    def _getfromapi(self, keywords: str = None, page: int = 1):
        self.url = "https://api.superjob.ru/2.0/vacancies/"
        self.params = {
            "keywords": keywords,
            "page": page
        }
        headers = {"X-Api-App-Id": self.api_key}
        return requests.get(self.url, headers=headers, params=self.params)
