# SPb Realty Mining

Если вы хотите снять квартиру в Петербурге, то неплохо бы сначала посмотреть что происходит 
с рынком недвижимости. Обычно большинство объявлений публикуются в общей базе 
[pin7.ru](https://pin7.ru) и агентства скорее всего будут предлагать вам варианты оттуда.

Превратить текущий снимок этой базы в удобную для анализа CSV или показать актуальные
на текущий момент статистики по рынку и призван SPb Realty Mining.

_Для установки и работы требуется Python 3.5+_

### Установка
Для начала нужно склонировать репозиторий и установить зависимости:
```bash
git clone git@github.com:anatoly-chichikov/spb-realty-mining.git
cd spb-realty-mining
pip install -r requirements.txt
```

### Сбор
Далее собираем данные. Для этого необходимо получить вашу персональную сессию.
- залогиниться в pin7 под вашим агентством или 
[общедоступным паролем](http://pin7-kod.ru/rukovodstvo-k-pin7-ru/)
- после логина нужно кликнуть `Cмотреть Базу`
- в инспекторе браузера найти cookies у запроса `https://pin7.ru/online.php`, 
например: `Cookie: pcode=imvcn7cdnsrqqm0crsl4ubkpp1`
- получить значение cookie `pcode`
- начать сбор и дождаться окончания (~10 минут)
```bash
python3 -m realty --task gather --cookie imvcn7cdnsrqqm0crsl4ubkpp1
```

### Обработка
После сбора генерим нашу CSV - `data.csv`. Теперь можете самостоятельно фильтровать предложения
и отправить их id своему агенту. 
```bash
python3 -m realty --task transform
```

### Статистики
Если имеется готовая CSV, можно посмотреть основные статистики по рынку:
```bash
python3 -m realty --task stats
```
