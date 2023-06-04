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
    def delete_vacancy(self, query=None) -> None:
        """Удаляет вакансию из файлв"""
        pass

    @abstractmethod
    def search(self, query=None) -> None:
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

    def delete_vacancy(self, query=None) -> None:
        """Удаляет вакансию из файлв"""
        try:
            old_jobs_list = self._open_file(self.filename)
        except json.decoder.JSONDecodeError:
            # Удалять нечего
            return

        if not query:
            # Нет критериев удаления
            return

        new_jobs_list = []
        for job in old_jobs_list:
            if not all(job.get(key) == value for key, value in query.items()):
                new_jobs_list.append(job)

        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(new_jobs_list, file, indent=4, ensure_ascii=False)


    def search(self, query: dict = None) -> None:
        """Выбирает данные из вакансий по криетриям
        Параметр
        query - словарь криериев значений для поиска
        Пример: query = {"city": "Минск", "salary": [10000, 50000]} - Город Минск с зарплатой от 10000 до 50000"""
        try:
            old_jobs_list = self._open_file(self.filename)
        except json.decoder.JSONDecodeError:
            # Выбирать нечего
            return []

        if not query:
            # Нет критериев поиска, значит возвращаем все
            return old_jobs_list

        new_jobs_list = []
        for job in old_jobs_list:
            if all(job.get(key)[0] <= value <= job.get(key)[1] if isinstance(job.get(key), list) else job.get(key) == value
                   for key, value in query.items()):
            # if all(job.get(key) == value for key, value in query.items()):/
                new_jobs_list.append(job)

        return new_jobs_list


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

vac = Vacancies(os.path.join("data", "jobs.json"))
# vac.delete_vacancy({"city": "Минск"})/
print(vac.search({"city": "Минск", "salary": [10000, 100000]}))