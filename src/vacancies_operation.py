from abc import ABC, abstractmethod
import json
import os

class VacanciesOperation(ABC):
    """ Класс для выполнения операций с множеством вакансий"""

    @adstractmethod
    def add_vacancy(self):
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


# class FileManager:
#
#     def printj(dict_to_print: dict) -> None:
#         """Выводит словарь в json-подобном удобном формате с отступами"""
#         print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))
#
#
#     @staticmethod
#     def _connect(filename) -> None:
#
#         if not os.path.exists(os.path.dirname(filename)):
#             os.mkdir(os.path.dirname(filename))
#
#         if not os.path.exists(filename):
#             with open(filename, 'w') as file:
#                 file.write(json.dumps([]))
#
#     @staticmethod
#     def _open_file(filename) -> list:
#
#         with open(filename, 'r', encoding="utf-8") as file:
#             return json.load(file)





