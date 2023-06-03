from abc import ABC, abstractmethod
import json
import os
from file_manager import FileManager


class VacanciesOperation(ABC):
    """ Класс для выполнения операций с множеством вакансий"""

    @adstractmethod
    def add_vacancy(self, vacancy_d):
        """Добавляет вакансию в файл"""
        pass

    @adstractmethod
    def delete_vacancy(self):
        """Удаляет вакансию из файлв"""
        pass

    @adstractmethod
    def search(self):
        """Выбирает данные из вакансий по криетриям"""
        pass


class Vacancies(VacanciesOperation, FileManager):
    """Основной класс для операций с ваканчиями"""

    @adstractmethod
    def add_vacancy(self, vacancy_dic):
        """Добавляет вакансию в файл"""
        # Добавляем данные для HH
        title =

    @adstractmethod
    def delete_vacancy(self):
        """Удаляет вакансию из файлв"""
        pass

    @adstractmethod
    def search(self):
        """Выбирает данные из вакансий по криетриям"""
        pass