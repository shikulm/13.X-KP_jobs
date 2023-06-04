from vacancy import Vacancy
import statistics
from vacancies_operation import Vacancies, VacanciesHH, VacanciesSJ


def sorting(vacancies: list[Vacancy]) -> list[Vacancy]:
    """Сортировка вакансий по убыванию"""
    return sorted(vacancies)

def get_top(vacancies: list[Vacancy], top_count: int) -> list[Vacancy]:
    """Сортировка вакансий по убыванию"""
    return sorted(vacancies, reverse=True)[:top_count]

def get_statistics(vacancies: list[Vacancy]) -> dict:
    """Вычисляет стастику по списку вакансий"""
    cnt = len(vacancies)
    salary_lst = [el["salary"] for el in vacancies if el["salary"] is not None]
    min_salary = min(salary_lst)
    max_salary = max(salary_lst)
    avg_salary = round(statistics.mean(salary_lst), 2)

    return {"cnt": cnt, "min_salary": min_salary, "max_salary": max_salary, "avg_salary": avg_salary}




