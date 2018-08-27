# coding=utf-8
import re
from datetime import datetime


def clean_id(crude_row):
    return int(crude_row.select('td.tdm_11')[0].text)


def clean_room(room):
    room = room.lower()

    if u'студия' in room:
        room = u's'
    elif room.startswith(u'2к.кв'):
        room = u'f2'
    elif room.startswith(u'3к.кв'):
        room = u'f3'
    elif room.startswith(u'4к.кв'):
        room = u'f4'
    elif room.startswith(u'к2('):
        room = u'r2'
    elif room.startswith(u'к3('):
        room = u'r3+'
    elif room.startswith(u'1к.кв'):
        room = u'f1'
    elif u'комната' in room:
        room = u'r1'
    elif u'дом' in room:
        room = u'h'
    elif u'к.кв' in room:
        room = u'f5+'
    else:
        room = u'o'

    return room


def clean_type(crude_row):
    soup = crude_row.select('td.tdm_01')[0]

    action = soup.select('font[color="#CC0033"]')[0].text.strip()

    room, date = (' '.join(x.split()) for x in soup.text.split(action))

    room = clean_room(room)
    date = datetime.strptime(date, '%H:%M %d.%m.%y')

    if action == u'сниму':
        action = 'rent'
    elif action == u'куплю':
        action = 'buy'
    elif action == u'продам':
        action = 'sell'
    elif action == u'сдам':
        action = 'rent_out'

    return {
        'action': action,
        'rooms': room,
        'create_date': date
    }


def clean_address(crude_row):
    soup = crude_row.select('td.tdm_02')[0]

    crude_district = soup.select('span.tdm_rn')[0].text
    crude_note = soup.select('em')

    note = ''

    if len(crude_note) > 0:
        note = crude_note[0].text.strip()

    district = [d.strip() for d in crude_district.replace(u'р-н', '').split(',')][0].lower()
    street = ' '.join(soup.text
                      .replace(crude_district, '')
                      .replace(u'на карте', '')
                      .replace(note, '')
                      .split()).lower()

    return {
        'district': district,
        'street': street
    }


def clean_subway(crude_row):
    soup = crude_row.select('td.tdm_03')[0]
    stations = soup.select('div[style^="margin-bottom"]')

    result = []

    for station in stations:
        crude_distance = station.select('span[style^="color"]')
        computed_distance = 0

        distance_to_replace = ''

        if len(crude_distance) > 0:
            found_distance = crude_distance[0].text
            distance_to_replace = found_distance

            if u'км' in found_distance:
                computed_distance = float(found_distance.strip().split()[0]) * 1000
            else:
                computed_distance = float(found_distance.strip().split()[0])

        name = station.text.replace(distance_to_replace, '').replace(',', '').strip().lower()

        result.append({
            'name': name,
            'distance': computed_distance
        })

    return sorted(result, key=lambda s: s['distance'])


def clean_price(crude_row):
    crude_price = crude_row.select('td.tdm_05')[0]

    crude_note = crude_price.select('span[style^="font-size:11px"]')

    note = ''

    if len(crude_note) > 0:
        note = crude_note[0].text.strip()

    crude_em = crude_price.select('em')

    em = ''

    if len(crude_em) > 0:
        em = crude_em[0].text.strip()

    split_price = crude_price.text.replace(note, '').replace(em, '').split()

    amount = int(split_price[0].replace('.', ''))
    period = 'unknown'

    if len(split_price) == 2:
        period_abbr = split_price[1]

        if period_abbr == u'руб/сут':
            period = 'daily'
        elif period_abbr == u'руб/мес':
            period = 'monthly'
        elif period_abbr == u'руб':
            period = 'once'

    return {
        'amount': amount,
        'period': period
    }


def clean_size(crude_options):
    size = 0

    if len(crude_options.select('strong')) > 0:
        crude_size = crude_options.select('strong')[0].text.strip().lower()

        if crude_size == '?':
            size = 0
        elif re.search(u'[а-я]+', crude_size):
            size = 0
        elif '+' in crude_size:
            size = sum([
                float(num)
                for num in crude_size.replace('(', '').replace(')', '').split('+')
                if num.isdigit()
            ])
        elif ',' in crude_size:
            size = sum([
                float(num.strip())
                for num in crude_size.replace('(', '').replace(')', '').split(',')
                if num.isdigit()
            ])
        else:
            size = float(crude_size)

    return size


def clean_floors(crude_options):
    text_opts = crude_options.text
    prepared = [
        x.strip()
        for x in text_opts.split('\n')
        if u'эт' in x
    ]

    if not prepared:
        return 0, 0

    floors = [
        x.replace(u'эт', '').strip()
        for x in prepared[0].split(',')
        if u'эт' in x
    ]

    floor, total_floors = floors[0].split('/')

    if total_floors == '?':
        total_floors = 0
    else:
        total_floors = int(total_floors)

    if floor == '-':
        floor = 1
    elif floor.lower() == u'цок':
        floor = -1
    elif floor.lower() == u'подв':
        floor = -1
    elif floor.lower() == u'манс':
        floor = total_floors
    elif floor.lower() == u'белэт':
        floor = 2
    elif floor.lower() == '?':
        floor = 0
    elif floor.lower() == u'техэт':
        floor = 0
    elif floor.lower() == u'все':
        floor = total_floors
    else:
        floor = int(floor)

    return floor, total_floors


def clean_options(crude_row):
    crude_options = crude_row.select('td.tdm_04')[0]

    size = clean_size(crude_options)
    floor, total_floors = clean_floors(crude_options)

    prepared = ' '.join([
        x.strip()
        for x in crude_options.text.split('\n')
        if x.strip()
    ]).split(u' эт')

    tags = []

    if len(prepared) is 2:
        tags = [tag.strip() for tag in prepared[1].lower().replace(u'жф', '').split(',')]

    has_elevator = False
    has_balcony = False
    house_state = 'old'

    for tag in tags:
        if u'лдж' in tag:
            has_balcony = True
        if u'блк' in tag:
            has_balcony = True
        if u'есть лифт' in tag:
            has_elevator = True
        if u'новый дом' in tag:
            house_state = 'new'
        if u'сф пкр' in tag:
            house_state = 'renovated'

    return {
        'house_state': house_state,
        'size': size,
        'floor': floor,
        'total_floors': total_floors,
        'has_elevator': has_elevator,
        'has_balcony': has_balcony
    }


def clean_notes(crude_row):
    crude_notes = crude_row.select('td.tdm_08')[0]

    all_notes = [
        note.strip().lower()
        for note in re.split(',|\n|\\|', crude_notes.text)
        if note.strip() != '' and u'комиссия' not in note.lower() and '+' not in note
    ]

    cool_renovation = False
    clean_front = False
    has_furniture = False
    has_tv = False
    has_fridge = False
    has_washer = False
    has_network_access = False
    has_dishwasher = False
    allowed_children = True
    allowed_pets = False
    has_parking = False

    for note in all_notes:
        if u'есть хол-к' in note:
            has_fridge = True
        if u'есть инт' in note:
            has_network_access = True
        if u'есть меб' in note:
            has_furniture = True
        if u'есть ст/маш' in note:
            has_washer = True
        if u'есть тв' in note:
            has_tv = True
        if u'посудом/маш' in note or u'встр посудом/маш' in note:
            has_dishwasher = True
        if u'без/дет' in note or u'без/мал/дет' in note:
            allowed_children = False
        if u'можно с животн' in note or u'с животн' in note:
            allowed_pets = True
        if u'паркинг' in note or u'парковка' in note:
            has_parking = True
        if u'чистая парадная' in note \
                or u'нов/дом' in note \
                or u'нов/квартал' in note \
                or u'элитн/дом' in note \
                or u'квартира бизнес-класса' in note \
                or u'дом бизнес-класса' in note \
                or u'элитный жил/компл' in note:
            clean_front = True
        if u'евро/рем' in note \
                or u'квартира бизнес-класса' in note \
                or u'элитный жил/компл' in note \
                or u'высок кач-во внутр/отд-ки' in note \
                or u'дизайнерский интерьер' in note \
                or u'дизайн' in note \
                or u'идеальн/сост' in note \
                or u'отл/сост' in note \
                or u'элитн/дом' in note \
                or u'дом бизнес-класса' in note:
            cool_renovation = True

    return {
        'cool_renovation': cool_renovation,
        'clean_front': clean_front,
        'has_furniture': has_furniture,
        'has_tv': has_tv,
        'has_fridge': has_fridge,
        'has_washer': has_washer,
        'has_network_access': has_network_access,
        'has_dishwasher': has_dishwasher,
        'allowed_children': allowed_children,
        'allowed_pets': allowed_pets,
        'has_parking': has_parking
    }


def clean_row(row):
    clean = {
        '_id': clean_id(row),
        'type': clean_type(row),
        'address': clean_address(row),
        'subway': clean_subway(row),
        'price': clean_price(row),
        'options': clean_options(row).update(clean_notes(row))
    }

    return clean
