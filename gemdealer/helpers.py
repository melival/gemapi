from django.db.models import Sum


def save_data(Model, data):
    Model(**data).save()
    # print(data)


def upload_from_csv(data, Model):
    t = data.split('\r\n')
    header, table = t[0], t[1:]
    print(header)

    rows = [row.split(',') for row in table if row]
    for customer, item, total, quantity, date in rows:
        data = {
            'customer': customer,
            'item': item,
            'total': int(total),
            'quantity': int(quantity),
            'date': date,
        }
        save_data(Model, data)

    return {'status': "Ok"}


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


def get_data(Model=None):
    # Выбираем любимых покупателей
    result = get_customers( (Model.objects.values('customer').
                                           annotate(summary=Sum('total')).
                                           order_by('-summary')
                            )[:5] )

    # Заполняем списки купленных камней
    for uname in result.keys():
        q = Model.objects.filter(customer=uname).values_list('item', flat=True)
        result.get(uname).get('gems').update(q)

    # Выбираем популярные камни
    pop_gems = get_popular_gems(result)
    for customer in result.values():
        customer.get('gems').intersection_update(pop_gems)

    return {'response': result}
