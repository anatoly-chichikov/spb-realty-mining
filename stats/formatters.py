import locale
from typing import Iterable

locale.setlocale(locale.LC_ALL, '')


def price(num: float) -> str:
    return "{0:n} ₽/мес".format(int(num))


def square(num: float) -> str:
    return "{0} кв.м.".format(round(num, 2))


def flat(num: float) -> str:
    return "{0:n} квартир".format(int(num))


def perc(num: float) -> str:
    return "{0}%".format(round(num, 2))


def districts(names: Iterable[str]) -> str:
    return ", ".join([name.capitalize() for name in names])
