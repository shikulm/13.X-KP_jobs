## Проект “Парсер вакансий”

## Описание

Программа, которая получает информацию о вакансиях с разных платформ в России, сохранять ее в файл и позволять удобно работать с ней (добавлять, фильтровать, удалять).

## Платформы для сбора вакансий

1. **hh.ru** ([ссылка на API](https://github.com/hhru/api/blob/master/docs/general.md))
2. **superjob.ru** ([ссылка на API](https://api.superjob.ru/))
    - Прежде чем начать использовать API от SuperJob, необходимо [зарегистрироваться](https://www.superjob.ru/auth/login/?returnUrl=https://api.superjob.ru/register/) и получить токен для работы. Подробная инструкция дается по ссылке описания документации в разделе [Getting started](https://api.superjob.ru/#gettin). При регистрации приложения можно указать произвольные данные.

## Выходные данные

- Информация о вакансиях, полученная с разных платформ, сохраненная в JSON-файл.
- Отфильтрованные и отсортированные вакансии, выводимые пользователю через консоль.

## Пример использования

Данный пример можно использовать как подсказку к началу реализации. Итоговая реализация может иметь любое количество классов, функций и их названий, другой принцип организации.

# Создание экземпляра класса для работы с API сайтов с вакансиями
hh_api = HeadHunterAPI()
superjob_api = SuperJobAPI()

# Получение вакансий с разных платформ
hh_vacancies = hh_api.get_vacancies("Python")
superjob_vacancies = superjob_api.get_vacancies("Python")

# Создание экземпляра класса для работы с вакансиями
vacancy = Vacancy("Python Developer", "<https://hh.ru/vacancy/123456>", "100 000-150 000 руб.", "Требования: опыт работы от 3 лет...")

# Сохранение информации о вакансиях в файл
json_saver = JSONSaver()
json_saver.add_vacancy(vacancy)
json_saver.get_vacancies_by_salary("100 000-150 000 руб.")
json_saver.delete_vacancy(vacancy)

# Функция для взаимодействия с пользователем
def user_interaction():
    platforms = ["HeadHunter", "SuperJob"]
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    filtered_vacancies = filter_vacancies(hh_vacancies, superjob_vacancies, filter_words)

    if not filtered_vacancies:
        print("Нет вакансий, соответствующих заданным критериям.")
        return

    sorted_vacancies = sort_vacancies(filtered_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()

