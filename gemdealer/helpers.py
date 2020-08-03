from django.db.models import Sum
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware


def csv_reader(data):
    """Парсинг csv файла.
    Стандартный csv.reader с первого раза не заработал - написал свой.
    """
    t = data.split('\r\n')
    if len(t) < 2: # Если строчек мало получилось
        raise RuntimeError("No data in csv source.")

    header, table = t[0], t[1:]
    rows = [row.split(',') for row in table if row]
    return header, rows


def save_row(Model, data):
    Model(**data).save()


def save_data(rows, Model):
    for customer, item, total, quantity, date in rows:
        data = {
            'customer': customer,
            'item': item,
            'total': int(total),
            'quantity': int(quantity),
            'date': make_aware(parse_datetime(date)),
        }
        save_row(Model, data)


def upload_from_csv(data, Model):
    try:
        _, rows = csv_reader(data)
        Model.objects.all().delete() # Про требование №2.
        save_data(rows, Model)
    except Exception as e:
        return {'Status': "Error", 'Desc': "Can't render csv data."}

    return {'Status': "Ok"}


def get_customers(query):
    result = dict()

    for i in query:
        username = i.get('customer')
        result[username] = {
            'username': username,
            'spent_money': i.get('summary'),
            'gems': set()
        }
    return result


def get_popular_gems(query):
    gems_counts = dict()
    gem_sets = [i.get('gems', set()) for i in query.values()]
    for gems in gem_sets:
        for gem in gems:
            gems_counts[gem] = gems_counts.get(gem, 0) + 1
    return set([gem for gem in gems_counts.keys() if gems_counts[gem] > 1])


def get_data(Model):
    # Выбираем любимых покупателей
    result = get_customers(
        ( Model.objects.values('customer').
                        annotate(summary=Sum('total')).
                        order_by('-summary')
        )[:5] )

    # Заполняем списки купленных камней
    for uname in result.keys():
        q = ( Model.objects.filter(customer=uname).
                            values_list('item', flat=True).
                            distinct() )
        result.get(uname).get('gems').update(q)

    # Выбираем популярные камни
    pop_gems = get_popular_gems(result)
    for customer in result.values():
        customer.get('gems').intersection_update(pop_gems)

    return {'response': result}
