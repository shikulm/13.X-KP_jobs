from abc import ABC, abstractmethod
class Vacancy:
    """Абстрактный класс с описанием вакансий"""

    __slots__ = ["__title", "__link", "__description", "__salary", "__city"]

    def __init__(self, title: str, link: str, description: str, salary: float, city: str, source: str) -> None:
        """Инициализируем описание вакансии основными характеристками"""
        self.title = title
        self.link = link
        self.description = description
        self.salary = salary
        self.city = city
        self.source = source

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__slots__})"

    def __str__(self):
        return f"Вакансия {self.title} из города {self.city} с зарплатой {self.salary} ({self.description})"

    def __gt__(self, other) -> bool:
        try:
            sal1 = 0 if self.salary is None else self.salary
            sal2 = 0 if other.salary is None else other.salary
            return sal1 > sal2
        except AttributeError:
            return False

    def __lt__(self, other) -> bool:
        try:
            sal1 = 0 if self.salary is None else self.salary
            sal2 = 0 if other.salary is None else other.salary
            return sal1 < sal2
        except AttributeError:
        return False

    def __eq__(self, other) -> bool:
        try:
            sal1 = 0 if self.salary is None else self.salary
            sal2 = 0 if other.salary is None else other.salary
            return sal1 == sal2
        except AttributeError:
            return False


    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, vtitle):
        if isinstance(vtitle, str):
            self.__title = vtitle

    @property
    def link(self):
        return self.__link

    @link.setter
    def link(self, vlink):
        if isinstance(vlink, str):
            self.__link = vlink

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, vdescription):
        if isinstance(vdescription, str):
            self.__description = vdescription


    @property
    def salary(self):
        return self.__salary

    @salary.setter
    def salary(self, vsalary):
        if isinstance(vsalary, float) or isinstance(vsalary, int) or vsalary is None:
            self.__salary = vsalary
        if vsalary < 0:
            self.__salary = 0

    @property
    def city(self):
        return self.__city

    @city.setter
    def city(self, vcity):
        if isinstance(vcity, str):
            self.__city = vcity


# title: str, link: str, description: str, salary: float, city: str
j1 = Vacancy("Программст", "https:/", "нужно проагрммировать", None, "Астрахань", 'HH')
print(repr(j1))
print(j1)
print()

j2 = Vacancy("Дворник", "https:/", "нужно убирать двор", 100000, "Астрахань", 'SJ')
print(repr(j2))
print(j2)
print()
print(f"j1>j2: {j1>j2}")
print(f"j1>0: {j1>0}")
# print(f"j1>=j2: {j1>=j2}")
print(f"j1<j2: {j1<j2}")
# print(f"j1<=j2: {j1<=j2}")
print(f"j1==j2: {j1==j2}")
