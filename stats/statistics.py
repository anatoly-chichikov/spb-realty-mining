from stats.filters import MonthlyRent
from stats.formatters import flat, perc, price, square
from stats.summary import Summary, logger


class General(Summary):

    def __init__(self, monthly: MonthlyRent) -> None:
        self._monthly = monthly

    def stats(self) -> None:
        rows = self._monthly.rows()

        logger.info('> Общая информация:')

        total = len(rows)
        room_total = len(rows[rows['type.rooms'].isin(['r1', 'r2', 'r3'])])
        one_bedroom_total = len(rows[rows['type.rooms'].isin(['f1', 's'])])
        two_bedroom_total = len(rows[rows['type.rooms'].isin(['f2'])])
        several_bedroom_total = len(rows[rows['type.rooms'].isin(['f3', 'f4', 'f5+'])])
        room_percents = room_total / total * 100.
        one_bedroom_percents = one_bedroom_total / total * 100.
        two_bedroom_percents = two_bedroom_total / total * 100.
        several_bedroom_percents = several_bedroom_total / total * 100.

        logger.info('===> Всего предложений - %s', flat(total))

        logger.info(
            '===> Комнаты - %s, %s',
            flat(room_total),
            perc(room_percents)
        )
        logger.info(
            '===> Однокомнатные и студии - %s, %s',
            flat(one_bedroom_total),
            perc(one_bedroom_percents)
        )
        logger.info(
            '===> Двухкомнатные - %s, %s',
            flat(two_bedroom_total),
            perc(two_bedroom_percents)
        )
        logger.info(
            '===> Три и более комнат - %s, %s',
            flat(several_bedroom_total),
            perc(several_bedroom_percents)
        )

        logger.info('===> В новостройках - %s', flat(len(rows[(rows['options.house_state'] == 'new')])))
        logger.info('===> С хорошим ремонтом - %s', flat(len(rows[(rows['options.cool_renovation'] == True)])))
        logger.info('===> Можно с детьми - %s', flat(len(rows[(rows['options.allowed_children'] == True)])))
        logger.info('===> Можно с животными - %s', flat(len(rows[(rows['options.allowed_pets'] == True)])))


class Prices(Summary):

    def __init__(self, monthly: MonthlyRent) -> None:
        self._monthly = monthly

    def stats(self) -> None:
        rows = self._monthly.rows()

        valuable = rows[rows['price.amount'] > 0.]['price.amount']

        logger.info('> Цена:')
        logger.info('===> Минимально возможная цена - %s', price(valuable.min()))
        logger.info('===> Максимальная цена - %s', price(valuable.max()))
        logger.info('===> Средняя цена - %s', price(valuable.mean()))
        logger.info('===> Половина предложений дешевле - %s', price(valuable.median()))
        logger.info('===> Большая часть (90%%) дешевле - %s', price(valuable.quantile(.9)))
        logger.info('===> Большая часть (90%%) дороже - %s', price(valuable.quantile(.1)))


class Squares(Summary):

    def __init__(self, monthly: MonthlyRent) -> None:
        self._monthly = monthly

    def stats(self) -> None:
        rows = self._monthly.rows()

        valuable = rows[rows['options.size'] > 0.]['options.size']

        logger.info('> Площадь:')
        logger.info('===> Минимально возможная площадь - %s', square(valuable.min()))
        logger.info('===> Максимальная площадь - %s', square(valuable.max()))
        logger.info('===> Средняя площадь - %s', square(valuable.mean()))
        logger.info('===> Половина предложений меньше - %s', square(valuable.median()))
        logger.info('===> Большая часть (90%%) меньше - %s', square(valuable.quantile(.9)))
        logger.info('===> Большая часть (90%%) больше - %s', square(valuable.quantile(.1)))
