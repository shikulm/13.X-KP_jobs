import json
import os


class FileManager:
    """Класс для работы с файлами"""

    def __init__(self, filename):
        """Сохраняет имя файла, с которым выполняется работа"""
        self.filename = filename

    @property
    def filename(self):
        return self._filename


    @filename.setter
    def filename(self, filename):
        # Сохраняет имя файла, с которым выполняется работа
        self._filename = filename
        # Создаем файл, если его нет
        self._connect(filename)

    @staticmethod
    def printj(dict_to_print: dict) -> None:
        """Выводит словарь в json-подобном удобном формате с отступами"""
        return json.dumps(dict_to_print, indent=2, ensure_ascii=False)

    @staticmethod
    def _connect(filename) -> None:
        """Проверяет существование файла. Если его нет, то создается пустой файл"""

        if not os.path.exists(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))

        if not os.path.exists(filename):
            with open(filename, 'w') as file:
                file.write(json.dumps([]))

    @staticmethod
    def _open_file(filename) -> list:
        """Читает данные из файла filename в формате Json"""

        with open(filename, 'r', encoding="utf-8") as file:
            return json.load(file)

    def bulk_insert(self, data):
        """Сохраняет данные data в файл"""
        with open(self._filename, "w", encoding="utf-8") as file:
            file.write(self.printj(data))



