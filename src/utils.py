from src.service_api import *
from vacancy import Vacancy
from vacancies_operation import Vacancies


def save_hh(keywords, page_start=0, page_count=2):
    """Сохраняет все считанные вакансии из HH  в файл"""
    hh = HH("Программист", page_start)

    vac = []
    for page in range(page_start, page_start+page_count+1):
        for item in hh._get_from_api().json()["items"]:

            dic_vac = {"title": item["name"],
                       "link": item["alternate_url"],
                       "description": item["snippet"]['requirement'],
                       "salary": item["salary"]["from"] if item.get("salary") else None,
                       "city": item["area"]["name"]}


hh = HH("Программист", 0)

vac = []
for item in hh._get_from_api().json()["items"]:
    # dic_vac = {"title": item["name"],
    #            "link": item["alternate_url"],
    #            "description": item["snippet"],
    #            "salary": item["salary"]["from"] if item.get("salary") else None,
    #            "city": item["address"]["city"]}

    dic_vac = {"title": item["name"],
               "link": item["alternate_url"],
               "description": item["snippet"]['requirement'],
               "salary": item["salary"]["from"] if item.get("salary") else None,
               "city": item["area"]["name"]}

    vac.append(dic_vac)

print(vac)

sj = SJ("Программист", 1)

vacsj = []
for item in sj._get_from_api().json()["objects"]:
    # dic_vac = {"title": item["name"],
    #            "link": item["alternate_url"],
    #            "description": item["snippet"],
    #            "salary": item["salary"]["from"] if item.get("salary") else None,
    #            "city": item["address"]["city"]}

    dic_vac = {"title": item["profession"],
               "link": item["link"],
               "description": item["candidat"],
               "salary": item["payment_from"],
               "city": item["town"]["title"]}

    vacsj.append(dic_vac)

print(vacsj)


hh.save_to_file(os.path.join("data", "hh.json"))
sj.save_to_file(os.path.join("data", "sj.json"))