# coding=utf-8
import re
from datetime import datetime


def clean_id(crude_row):
    return int(crude_row.select('td.tdm_11')[0].text)


def clean_room(room):
    room = room.lower()

    if 'студия' in room:
        room = 's'
    elif room.startswith('2к.кв'):
        room = 'f2'
    elif room.startswith('3к.кв'):
        room = 'f3'
    elif room.startswith('4к.кв'):
        room = 'f4'
    elif room.startswith('к2('):
        room = 'r2'
    elif room.startswith('к3('):
        room = 'r3+'
    elif room.startswith('1к.кв'):
        room = 'f1'
    elif 'комната' in room:
        room = 'r1'
    elif 'дом' in room:
        room = 'h'
    elif 'к.кв' in room:
        room = 'f5+'
    else:
        room = 'o'

    return room


def clean_type(crude_row):
    soup = crude_row.select('td.tdm_01')[0]

    action = soup.select('font[color="#CC0033"]')[0].text.strip()

    room, date = (' '.join(x.split()) for x in soup.text.split(action))

    room = clean_room(room)
    date = datetime.strptime(date, '%H:%M %d.%m.%y')

    if action == 'сниму':
        action = 'rent'
    elif action == 'куплю':
        action = 'buy'
    elif action == 'продам':
        action = 'sell'
    elif action == 'сдам':
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

    district = [d.strip() for d in crude_district.replace('р-н', '').split(',')][0].lower()
    street = ' '.join(soup.text
                      .replace(crude_district, '')
                      .replace('на карте', '')
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

            if 'км' in found_distance:
                computed_distance = float(found_distance.strip().split()[0]) * 1000
            else:
                computed_distance = float(found_distance.strip().split()[0])

        name = station.text.replace(distance_to_replace, '').replace(',', '').strip().lower()

        result.append({
            'name': name,
            'distance': computed_distance
        })

    if not result:
        return {}

    return sorted(result, key=lambda s: s['distance'])[0]


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

        if period_abbr == 'руб/сут':
            period = 'daily'
        elif period_abbr == 'руб/мес':
            period = 'monthly'
        elif period_abbr == 'руб':
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
        elif re.search('[а-я]+', crude_size):
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
        if 'эт' in x
    ]

    if not prepared:
        return 0, 0

    floors = [
        x.replace('эт', '').strip()
        for x in prepared[0].split(',')
        if 'эт' in x
    ]

    floor, total_floors = floors[0].split('/')

    if total_floors == '?':
        total_floors = 0
    else:
        total_floors = int(total_floors.split(" ")[0])

    if floor == '-':
        floor = 1
    elif floor.lower() == 'цок':
        floor = -1
    elif floor.lower() == 'подв':
        floor = -1
    elif floor.lower() == 'манс':
        floor = total_floors
    elif floor.lower() == 'белэт':
        floor = 2
    elif floor.lower() == '?':
        floor = 0
    elif floor.lower() == 'техэт':
        floor = 0
    elif floor.lower() == 'все':
        floor = total_floors
    elif floor.lower().startswith('кух'):
        floor = int(floor.split(' ')[1])
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
    ]).split(' эт')

    tags = []

    if len(prepared) is 2:
        tags = [tag.strip() for tag in prepared[1].lower().replace('жф', '').split(',')]

    has_elevator = False
    has_balcony = False
    house_state = 'old'

    for tag in tags:
        if 'лдж' in tag:
            has_balcony = True
        if 'блк' in tag:
            has_balcony = True
        if 'есть лифт' in tag:
            has_elevator = True
        if 'новый дом' in tag:
            house_state = 'new'
        if 'сф пкр' in tag:
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
        if note.strip() != '' and 'комиссия' not in note.lower() and '+' not in note
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
        if 'есть хол-к' in note:
            has_fridge = True
        if 'есть инт' in note:
            has_network_access = True
        if 'есть меб' in note:
            has_furniture = True
        if 'есть ст/маш' in note:
            has_washer = True
        if 'есть тв' in note:
            has_tv = True
        if 'посудом/маш' in note or 'встр посудом/маш' in note:
            has_dishwasher = True
        if 'без/дет' in note or 'без/мал/дет' in note:
            allowed_children = False
        if 'можно с животн' in note or 'с животн' in note:
            allowed_pets = True
        if 'паркинг' in note or 'парковка' in note:
            has_parking = True
        if 'чистая парадная' in note \
                or 'нов/дом' in note \
                or 'нов/квартал' in note \
                or 'элитн/дом' in note \
                or 'квартира бизнес-класса' in note \
                or 'дом бизнес-класса' in note \
                or 'элитный жил/компл' in note:
            clean_front = True
        if 'евро/рем' in note \
                or 'квартира бизнес-класса' in note \
                or 'элитный жил/компл' in note \
                or 'высок кач-во внутр/отд-ки' in note \
                or 'дизайнерский интерьер' in note \
                or 'дизайн' in note \
                or 'идеальн/сост' in note \
                or 'отл/сост' in note \
                or 'элитн/дом' in note \
                or 'дом бизнес-класса' in note:
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
    options = clean_options(row)
    options.update(clean_notes(row))
    
    clean = {
        'id': clean_id(row),
        'type': clean_type(row),
        'address': clean_address(row),
        'subway': clean_subway(row),
        'price': clean_price(row),
        'options': options  
    }

    return clean
