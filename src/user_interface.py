from vacancies_operation import Vacancies, VacanciesSJ, VacanciesHH, Vacancy
import os
import json
import utils
class UserInterface:
    """Класс с пользовательским интерфейсом"""

    def hello(self):
        """Функция приветсвия"""
        print("Здравствуйте!!!")
        print("Перед вами программа для парсинга вакансий.")
        print("Вакансии парсятся с двух сайтов - Head Hunter и Suprjob")
        print()


    def print_vacancies(self, vacancies: list[Vacancy]) -> None:
        """Вывод на экран вакансий"""
        [print(el) for el in vacancies]

    def get_keyword(self):
        print(f"Введите ключевые слова для поиска вакансий. \nДля нескольких ключевых слов в качестве разделителя используйте запятую")
        self.keywords = input(">> ")
        self.page_count = 2

        # Сохраняем вакансии в файл
        hh_vacancies = VacanciesHH(self.filename)
        hh_vacancies.clear_data()
        hh_vacancies.save_api_to_file(self.keywords, 0, 2)
        sj_vacancies = VacanciesSJ(self.filename)
        sj_vacancies.save_api_to_file(self.keywords, 1, 2)

        self.vacancies = Vacancies(self.filename)

        # Проверяем были ли найдены значения для ключевых слов
        if len(self.vacancies.search()) > 0:
            # Данные найдены
            return True
        else:
            # Данных нет
            print("Для вашего запроса данные не найдены!")
            return False

        # try:
        #     # Данные найдены
        #     jobs_list = self.vacancies.search()
        # except json.decoder.JSONDecodeError:
        #     # Данных нет
        #     return False

    def print_statistics(self, vacancies: list[Vacancy] = None) -> None:
        """Получение и вывод статистических данных"""
        if vacancies is None:
            vacancies = self.vacancies.search()
        stat_dic = utils.get_statistics(vacancies)
        print(f"Всего вакансий: {stat_dic['cnt']}.")
        print(f"Зарплаты от {stat_dic['min_salary']} до {stat_dic['max_salary']}.")
        print(f"Средняя зарплата {stat_dic['avg_salary']}.")

    def __init__(self, page_count=3):
        # Количество страниц из источника, по котрым нужно получать данные
        self.vacancies = None
        self.page_count = page_count
        # Имя файла, в котором будут храниться данные по вакансиям
        self.filename = os.path.join("data", "jobs.json")
        self.keywords = None
        self.hello()

        # Получаем данные из источника по ключевым словам
        if self.get_keyword():
            self.print_statistics(self.vacancies.search())
        else:
            return

ui = UserInterface()


# hh_vacancies = VacanciesHH(os.path.join("data", "jobs.json"))
# hh_vacancies.clear_data()
# hh_vacancies.save_api_to_file("Программист", 0, 2)
# sj_vacancies = VacanciesSJ(os.path.join("data", "jobs.json"))
# hh_vacancies.save_api_to_file("Программист", 1, 2)

vac = Vacancies(os.path.join("data", "jobs.json"))
# vac.delete_vacancy({"city": "Минск"})/
# print("\n".join(vac.search({"city": "Алматы", "salary": [None, 50000]})))
# print(vac.search({"city": "Алматы"}))
[print(el) for el in vac.search({"city": "Алматы", "salary": [None, 50000]})]