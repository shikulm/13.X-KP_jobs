from service_api import HH, SJ
from abc import ABC, abstractmethod
import json
import os
from file_manager import FileManager


class VacanciesOperation(ABC):
    """ Класс для выполнения операций с множеством вакансий"""

    @abstractmethod
    def add_vacancy(self, vacancy):
        """Добавляет вакансию в файл"""
        pass

    @abstractmethod
    def delete_vacancy(self):
        """Удаляет вакансию из файлв"""
        pass

    @abstractmethod
    def search(self):
        """Выбирает данные из вакансий по криетриям"""
        pass


class Vacancies(VacanciesOperation, FileManager):
    """Основной класс для операций с ваканcиями"""


    def add_vacancy(self, vacancy_dict: dict) -> None:
        """Добавляет вакансию в файл. В параметре указывается словарь значений"""
        #  Считываем старые значения из файла
        try:
            jobs_list = self._open_file(self.filename)
        except json.decoder.JSONDecodeError:
            jobs_list = []
            # jobs_list = [] if not self._open_file(self.filename) else self._open_file(self.filename)
        jobs_list.append(vacancy_dict)

        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(jobs_list, file, indent=4, ensure_ascii=False)
            # json.dump(self.printj(jobs_list), file)

    def delete_vacancy(self):
        """Удаляет вакансию из файлв"""
        pass

    def search(self):
        """Выбирает данные из вакансий по криетриям"""
        pass


class VacanciesHH(Vacancies):
    """Класс для работы с вакансиями из Head Hunter"""

    def save_api_to_file(self, keywords: str, page_start: int = 0, page_count: int = 2) -> None:
        """Сохраняет данные из api HH в файл. Учитывает только атрибуты, которые используются в классе с вакансиями
        Параметры
        filename: имя выходного файла,
        keywords - ключевые слова для поиска данных,
        page_start - с какой страницы извлекаем данные
        page_count - какое количество страниц созраняем"""
        # self.filename = filename
        for page in range(page_start, page_start + page_count + 1):
            hh = HH(keywords, page)
            for item in hh.get_from_api(keywords, page).json()["items"]:
                dic_vac = {"title": item["name"],
                           "link": item["alternate_url"],
                           "description": item["snippet"]['requirement'],
                           "salary": item["salary"]["from"] if item.get("salary") else None,
                           "city": item["area"]["name"],
                           "source": "HH"}
                self.add_vacancy(dic_vac)


class VacanciesSJ(Vacancies):
    """Класс для работы с вакансиями из Super Job"""

    def save_api_to_file(self, keywords: str, page_start: int = 1, page_count: int = 2) -> None:
        """Сохраняет данные из api HH в файл. Учитывает только атрибуты, которые используются в классе с вакансиями
        Параметры
        filename: имя выходного файла,
        keywords - ключевые слова для поиска данных,
        page_start - с какой страницы извлекаем данные
        page_count - какое количество страниц созраняем"""
        # self.filename = filename
        for page in range(page_start, page_start + page_count + 1):

            sj = SJ(keywords, page)
            for item in sj.get_from_api(keywords, page).json()["items"]:
                dic_vac = {"title": item["profession"],
                           "link": item["link"],
                           "description": item["candidat"],
                           "salary": item["payment_from"],
                           "city": item["town"]["title"],
                           "source": "SJ"}
                self.add_vacancy(dic_vac)


hh_vacancies = VacanciesHH(os.path.join("data", "jobs.json"))
hh_vacancies.save_api_to_file("Программист", 0, 2)
sj_vacancies = VacanciesSJ(os.path.join("data", "jobs.json"))
hh_vacancies.save_api_to_file("Программист", 1, 2)

        #
        # def save_hh(keywords, page_start=0, page_count=2):
        #     """Сохраняет все считанные вакансии из HH  в файл"""
        #     hh = HH("Программист", page_start)
        #
        #     for page in range(page_start, page_start + page_count + 1):
        #         for item in hh.get_from_api().json()["objects"]:
        #             dic_vac = {"title": item["name"],
        #                        "link": item["alternate_url"],
        #                        "description": item["snippet"]['requirement'],
        #                        "salary": item["salary"]["from"] if item.get("salary") else None,
        #                        "city": item["area"]["name"]}
        #
        # hh = HH("Программист", 0)
        #
        # vac = []
        # for item in hh.get_from_api().json()["items"]:
        #     # dic_vac = {"title": item["name"],
        #     #            "link": item["alternate_url"],
        #     #            "description": item["snippet"],
        #     #            "salary": item["salary"]["from"] if item.get("salary") else None,
        #     #            "city": item["address"]["city"]}
        #
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
        # for item in sj._get_from_api().json()["objects"]:
        #     # dic_vac = {"title": item["name"],
        #     #            "link": item["alternate_url"],
        #     #            "description": item["snippet"],
        #     #            "salary": item["salary"]["from"] if item.get("salary") else None,
        #     #            "city": item["address"]["city"]}
        #
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
        # hh.save_to_file(os.path.join("data", "hh.json"))
        # sj.save_to_file(os.path.join("data", "sj.json"))


