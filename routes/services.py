from trains.models import Train


def dfs_paths(graph, start, goal):
    """Функция поиска всех возможных маршрутов из одного города в другой. Вариант посещения одного и того же города
    более одного раза - НЕ рассматривается """
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == goal:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_]))


def get_graph(queryset):
    graph = {}
    for query in queryset:
        graph.setdefault(query.from_city_id, set())
        graph[query.from_city_id].add(query.to_city_id)
    return graph


def get_routes(request, form):
    context = {
        'form': form
    }

    queryset = Train.objects.all().select_related('from_city', 'to_city')
    graph = get_graph(queryset)
    data = form.cleaned_data
    from_city = data['from_city']
    to_city = data['to_city']
    time_travel = data['all_time']
    cities = data['cities']  # С формы
    all_ways = list(dfs_paths(graph, from_city.id, to_city.id))  # -> СПИСОК
    ''' [[2,4,5,6], [3, 5, 7, 6]] путь по городам от 2 до 6, от 3 до 6 через города '''

    if not len(all_ways):
        raise ValueError('Подходящего маршрута - НЕТ!')
    if cities:
        _cities = [city.id for city in cities]
        right_ways = []
        for way in all_ways:  # way - список с id городами
            if all(city in way for city in _cities):
                right_ways.append(way)
        if not right_ways:
            raise ValueError('Подходящего маршрута через эти города - НЕТ!')

    else:
        right_ways = all_ways

    routes = []
    all_trains = {}
    for query in queryset:
        all_trains.setdefault((query.from_city_id, query.to_city_id), [])
        all_trains[
            (query.from_city_id, query.to_city_id)
        ].append(query)

    for way in right_ways:
        temp = {}
        temp['trains'] = []
        total_time = 0
        for i in range(len(way) - 1):
            qs = all_trains[(way[i], way[i + 1])]
            q = qs[0]  # Берем экземпляр класса модели поезда
            total_time += q.travel_time
            temp['trains'].append(q)
        temp['total_time'] = total_time
        if total_time <= time_travel:
            routes.append(temp)
    if not routes:
        raise ValueError('Время в пути больше заданного')

    # Сортируем маршруты по времени
    sorted_routes = []
    if len(routes) == 1:
        sorted_routes = routes
    else:
        # total_time в каждом словаре - время маршрута , в routes словари temp
        times = list(set(r['total_time'] for r in routes)) # set т.к время может быть одинаковые у маршрутов
        times = sorted(times)
        for time in times:
            for route in routes:
                if time == route['total_time']:
                    sorted_routes.append(route)

    context['routes'] = sorted_routes
    context['cities'] = {'from_city': from_city, 'to_city': to_city}

    return context
