import argparse
import logging

logger = logging.getLogger(__name__)


class App:

    def __init__(self, args, crawling):
        self.args = args
        self.crawling = crawling

    def start(self):
        logger.info("Work started")

        args = self.args.parsed()

        if args.task == 'gather':
            self.gather_process(args.cookie)
        elif args.task == 'transform':
            self.convert_data_to_table_format()

        elif args.task == 'stats':
            self.stats_of_data()

        logger.info("Work ended")

    def gather_process(self, cookie):
        logger.info("gather")

        self.crawling.await(cookie)

    def convert_data_to_table_format(self):
        logger.info("transform")

    def stats_of_data(self):
        logger.info("stats")


class ShellArgs:

    @staticmethod
    def parsed():
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
