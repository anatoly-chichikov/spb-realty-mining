import argparse
import logging

from parsers.pin7 import ParsedPages
from scrappers.pin7 import CrawlingTask
from stats.summary import Statistics

logger = logging.getLogger(__name__)


class ShellArgs:

    @staticmethod
    def parsed() -> argparse.Namespace:
        cookie_help = """
        Обязателен для задачи gather!\n
        Чтобы начать сбор станиц, вы должны авторизоваться в pin7.ru и заполучить персональную куку.
        Получить её просто - зайти на pin7.ru, ввести любой валидный общедоступный пароль (например 777).
        В DevTools браузера посмотреть куки при запросе 'https://pin7.ru/online.php'.
        Нас интересует 'pcode', должна выглядеть примерно так: 'pcode=imvcn7cdnsrqqm0crsl4ubkpp1'.
        В итоге пишем для запуска сбора: 'python3 -m realty --task gather --cookie imvcn7cdnsrqqm0crsl4ubkpp1'.
        """
        task_help = """
        Вы можете выбрать одну из задач:
        gather - сбор информации из pin7.ru,
        transform - парсинг страниц и сохранение в CSV,
        stats - вывод основных статистик по полученному результату.
        Пример запуска: 'python3 -m realty --task stats'
        """
        parser = argparse.ArgumentParser()

        parser.add_argument('--task', required=True, help=task_help, choices=['gather', 'transform', 'stats'])
        parser.add_argument('--cookie', help=cookie_help)

        parsed = parser.parse_args()

        if (parsed.task == 'gather') and (parsed.cookie is None):
            raise argparse.ArgumentTypeError('--cookie is required for gather task')

        return parsed


class ChosenApp:

    def __init__(
            self,
            args: ShellArgs,
            crawling: CrawlingTask,
            parsed: ParsedPages,
            stats: Statistics
    ) -> None:
        self._args = args
        self._crawling = crawling
        self._parsed = parsed
        self._stats = stats

    def start(self) -> None:
        logger.info("Work started")

        args = self._args.parsed()

        if args.task == 'gather':
            self._gather_process(args.cookie)
        elif args.task == 'transform':
            self._convert_data_to_table_format()
        elif args.task == 'stats':
            self._stats_of_data()

        logger.info("Work ended")

    def _gather_process(self, cookie: str) -> None:
        logger.info("gather")
        self._crawling.wait(cookie)

    def _convert_data_to_table_format(self) -> None:
        logger.info("transform")
        self._parsed.save()

    def _stats_of_data(self) -> None:
        logger.info("stats")
        self._stats.print()
