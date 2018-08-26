"""
ЗАДАНИЕ

Выбрать источник данных и собрать данные по некоторой предметной области.

Цель задания - отработать навык написания программ на Python.
В процессе выполнения задания затронем области:
- организация кода в виде проекта, импортирование модулей внутри проекта
- unit тестирование
- работа с файлами
- работа с протоколом http
- работа с pandas
- логирование

Требования к выполнению задания:

- собрать не менее 1000 объектов

- в каждом объекте должно быть не менее 5 атрибутов
(иначе просто будет не с чем работать.
исключение - вы абсолютно уверены что 4 атрибута в ваших данных
невероятно интересны)

- сохранить объекты в виде csv файла

- считать статистику по собранным объектам


Этапы:

1. Выбрать источник данных.

Это может быть любой сайт или любое API

Примеры:
- Пользователи vk.com (API)
- Посты любой популярной группы vk.com (API)
- Фильмы с Кинопоиска
(см. ссылку на статью ниже)
- Отзывы с Кинопоиска
- Статьи Википедии
(довольно сложная задача,
можно скачать дамп википедии и распарсить его,
можно найти упрощенные дампы)
- Статьи на habrahabr.ru
- Объекты на внутриигровом рынке на каком-нибудь сервере WOW (API)
(желательно англоязычном, иначе будет сложно разобраться)
- Матчи в DOTA (API)
- Сайт с кулинарными рецептами
- Ebay (API)
- Amazon (API)
...

Не ограничивайте свою фантазию. Это могут быть любые данные,
связанные с вашим хобби, работой, данные любой тематики.
Задание специально ставится в открытой форме.
У такого подхода две цели -
развить способность смотреть на задачу широко,
пополнить ваше портфолио (вы вполне можете в какой-то момент
развить этот проект в стартап, почему бы и нет,
а так же написать статью на хабр(!) или в личный блог.
Чем больше у вас таких активностей, тем ценнее ваша кандидатура на рынке)

2. Собрать данные из источника и сохранить себе в любом виде,
который потом сможете преобразовать

Можно сохранять страницы сайта в виде отдельных файлов.
Можно сразу доставать нужную информацию.
Главное - постараться не обращаться по http за одними и теми же данными много раз.
Суть в том, чтобы скачать данные себе, чтобы потом их можно было как угодно обработать.
В случае, если обработать захочется иначе - данные не надо собирать заново.
Нужно соблюдать "этикет", не пытаться заддосить сайт собирая данные в несколько потоков,
иногда может понадобиться дополнительная авторизация.

В случае с ограничениями api можно использовать time.sleep(seconds),
чтобы сделать задержку между запросами

3. Преобразовать данные из собранного вида в табличный вид.

Нужно достать из сырых данных ту самую информацию, которую считаете ценной
и сохранить в табличном формате - csv отлично для этого подходит

4. Посчитать статистики в данных
Требование - использовать pandas (мы ведь еще отрабатываем навык использования инструментария)
То, что считаете важным и хотели бы о данных узнать.

Критерий сдачи задания - собраны данные по не менее чем 1000 объектам (больше - лучше),
при запуске кода командой "python3 -m gathering stats" из собранных данных
считается и печатается в консоль некоторая статистика

Код можно менять любым удобным образом
Можно использовать и Python 2.7, и 3

Зачем нужны __init__.py файлы
https://stackoverflow.com/questions/448271/what-is-init-py-for

Про документирование в Python проекте
https://www.python.org/dev/peps/pep-0257/

Про оформление Python кода
https://www.python.org/dev/peps/pep-0008/


Примеры сбора данных:
https://habrahabr.ru/post/280238/

Для запуска тестов в корне проекта:
python3 -m unittest discover

Для запуска проекта из корня проекта:
python3 -m gathering gather
или
python3 -m gathering transform
или
python3 -m gathering stats


Для проверки стиля кода всех файлов проекта из корня проекта
pep8 .

"""

import argparse
import logging

from scrapy.crawler import CrawlerProcess

from scrappers.scrapper import CrawlingTask
from storages.file_storage import FileStorage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCRAPPED_FILE = 'scrapped_data.txt'
TABLE_FORMAT_FILE = 'data.csv'


def parse_args():
    cookie_help = """
    Обязателен для задачи gather!\n
    Чтобы начать сбор станиц, вы должны авторизоваться в pin7.ru и заполучить персональную куку.
    Получить её просто - зайти на pin7.ru, ввести любой валидный общедоступный пароль (например 777).
    В DevTools браузера посмотреть куки при запросе 'https://pin7.ru/online.php'.
    Нас интересует 'pcode', должна выглядеть примерно так: 'pcode=imvcn7cdnsrqqm0crsl4ubkpp1'.
    В итоге пишем для запуска сбора: 'python3 -m gathering --task gather --cookie imvcn7cdnsrqqm0crsl4ubkpp1'.
    """
    task_help = """
    Вы можете выбрать одну из задач:
    gather - сбор информации из pin7.ru,
    transform - парсинг страниц и сохранение в CSV,
    stats - вывод основных статистик по полученному результату.
    Пример запуска: 'python3 -m gathering --task stats'
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--task', required=True, help=task_help, choices=['gather', 'transform', 'stats'])
    parser.add_argument('--cookie', help=cookie_help)

    parsed = parser.parse_args()

    if (parsed.task == 'gather') and (parsed.cookie is None):
        raise argparse.ArgumentTypeError('--cookie is required for gather task')

    return parsed


def gather_process(cookie):
    logger.info("gather")

    CrawlingTask(
        FileStorage(SCRAPPED_FILE),
        CrawlerProcess({
            'DOWNLOAD_DELAY': 1,
            'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) '
                          'AppleWebKit/605.1.15 (KHTML, like Gecko) '
                          'Version/11.1.2 Safari/605.1.15'
        })
    ).await(cookie)


def convert_data_to_table_format():
    logger.info("transform")
    storage = FileStorage(SCRAPPED_FILE)


def stats_of_data():
    logger.info("stats")

    # Your code here
    # Load pandas DataFrame and print to stdout different statistics about the data.
    # Try to think about the data and use not only describe and info.
    # Ask yourself what would you like to know about this data (most frequent word, or something else)


if __name__ == '__main__':
    """
    why main is so...?
    https://stackoverflow.com/questions/419163/what-does-if-name-main-do
    """
    args = parse_args()

    logger.info("Work started")

    if args.task == 'gather':
        gather_process(args.cookie)

    elif args.task == 'transform':
        convert_data_to_table_format()

    elif args.task == 'stats':
        stats_of_data()

    logger.info("Work ended")
