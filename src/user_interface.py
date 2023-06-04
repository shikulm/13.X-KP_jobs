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
        if len(vacancies) == 0:
            print("Вакансии не найдены")
        else:
            vacan = utils.sorting(vacancies)
            [print(el) for el in vacan]

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


    def print_statistics(self, vacancies: list[Vacancy] = None) -> None:
        """Получение и вывод статистических данных"""
        if vacancies is None:
            vacancies = self.vacancies.search()
        stat_dic = utils.get_statistics(vacancies)
        print(f"Всего вакансий: {stat_dic['cnt']}.")
        print(f"Зарплаты от {stat_dic['min_salary']} до {stat_dic['max_salary']}.")
        print(f"Средняя зарплата {stat_dic['avg_salary']}.")

    def __user_input(self, txt_quest: str, type: str ='str'):
        """Функция приглашает к вводу от пользователя запрос с определнным типом данных.
        Пользователь будет отвечать до тех пор, пока не введет корректное значение"""

        while True:
            us_sel = input(f"{txt_quest} >> ")
            if type == "int":
                try:
                    us_sel = int(us_sel)
                    return us_sel
                except ValueError:
                    print("Вы должны ввести число")
            else:
                return us_sel

    def print_top(self):
        """Выод top вакансий"""
        print("Какое количество вакансий с наибольшей зарплатой вы хотите получить?")
        while True:
            top_count = self.__user_input("", 'int')
            if top_count <= 0:
                print("Число должно быть положительным!")
            else:
                break

        vacan = utils.get_top(self.vacancies.search(), top_count)
        print()
        self.print_vacancies(vacan)
        print()
        self.print_statistics(vacan)


    def print_filter_vacacies(self):
        """Получение списка отфильтрованных вакансий"""
        # Список словарей для диалога с пользователем
        # title: str, link: str, description: str, salary: float, city: str, source: str
        query_user = [
            {"attr_name": "title",
             "attr_rus": "Название вакансии",
             "between": False,
             "options": "",
             "type": "str"},
            {"attr_name": "salary",
             "attr_rus": "Зарплата",
             "between": True,
             "options": "",
            "type": "int"
            },
            {"attr_name": "city",
             "attr_rus": "Город",
             "between": False,
             "options": "",
             "type": "str"},
            {"attr_name": "source",
             "attr_rus": "Источник",
             "between": False,
             "options": "'HH'/'SJ'",
             "type": "str"},
        ]

        # Вывод приглашения для выбора
        print("Выберите по каким признакам фильтровать списки вакансий.")
        print("Можно указать несколько номеров через пробел или 0 для отмены выбора:")

        while True:
            # Выводим варианты
            ind = 1
            for el in query_user:
                print(f"{ind} - {el['attr_rus']}")
                ind += 1
            print("0 - Отменить выбор")

            try:
                user_select = list(map(int, input(">> ").split()))

                if 0 in user_select:
                    # Прерываем выполнение, если пользователь решилд отказаться
                    return False

                # Запрашиваем значения у пользователя
                print("\nТеперь введите значения для поиска")

                query_dic = {}

                for ind in user_select:
                    id_q = ind-1

                    if query_user[id_q]["between"]:
                        # Пользователь вводит диапазон
                        us_sel1 = self.__user_input(f"{query_user[id_q]['attr_rus']} от ", query_user[id_q]['type'])
                        us_sel2 = self.__user_input(f"{query_user[id_q]['attr_rus']} до ", query_user[id_q]['type'])
                        if us_sel2 < us_sel1:
                            # Если верхняя граница меньше нижней, меняем их местами
                            us_sel = us_sel1
                            us_sel1 = us_sel2
                            us_sel1 = us_sel
                        query_dic[query_user[id_q]['attr_name']] = [us_sel1, us_sel2]
                    else:
                        # us_sel = input(f"{query_user[id_q]['attr_rus']} {query_user[id_q]['options']} >> ")
                        us_sel = self.__user_input(f"{query_user[id_q]['attr_rus']} {query_user[id_q]['options']}", query_user[id_q]['type'])
                        query_dic[query_user[id_q]['attr_name']] = us_sel

                # Получаем и выводим отфильтрованные данные
                print()
                vacancies_lst = self.vacancies.search(query_dic)
                self.print_vacancies(vacancies_lst)
                print()
                self.print_statistics(vacancies_lst)

                return True
            except ValueError:
                print("Вы должны ввести число")
                continue

            if not all([0 <= el <= len(query_user) for el in user_select]):
                print(f"Вы должны указать числа в интевале от 0 до {len(query_user)}")
                continue

    def main_menu(self):
        """Главное меню для выбора вариантов"""
        print()
        print("Выберите, что вы хотите получить?")
        print("1 - Статистику по вакансиям")
        print("2 - Список вакансий, отфильтрованный по вашим критериям")
        print("3 - Вакансии с наибольшей зарплатой")
        print("0 - Завершить работу")
        while True:
            us_sel = self.__user_input("", 'int')
            if us_sel not in range(4):
                print("Число должно быть от 1 до 3")
                continue
            else:
                if us_sel == 0:
                    return False
                elif us_sel == 1:
                    self.print_statistics()
                elif us_sel == 2:
                    self.print_filter_vacacies()
                elif us_sel == 3:
                   self.print_top()
                return True

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
            while True:
                print()
                if not self.main_menu():
                    print("Благодарим за использование нашей проагрммы!")
                    return
            # self.print_statistics(self.vacancies.search())

            # self.print_filter_vacacies()

            # self.print_top()
        else:
            return

ui = UserInterface()


