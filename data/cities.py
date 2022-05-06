import requests
from random import choice

# фото со спутника заданного адреса
def new_place(place):
    toponym_to_find = place
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        pass
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    a = [float(i) for i in toponym['boundedBy']['Envelope']['lowerCorner'].split()]
    b = [float(i) for i in toponym['boundedBy']['Envelope']['upperCorner'].split()]
    delta = [str(max(b[0], a[0]) - min(b[0], a[0])), str(max(b[1], a[1]) - min(b[1], a[1]))]
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        'z': coords(delta[0], delta[1]),
        "spn": ",".join([delta[0], delta[1]]),
        "l": "sat",
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    return response.url

# рандомный выбор города для игры
def city():
    spisok = [['Крассная площадь', 'Москва'], ['авеню Пьер Лоти, 12, VII округ Парижа, Париж, Франция', 'Париж'],
              ['Санкт-Петербург Дворцовая площадь', 'Санкт-Петербург'], ['Колизей Италия', 'Рим'],
              ['Россия Республика Татарстан Казань проезд Шейнкмана', 'Казань'],
              ['остров Свободы город Джерси-Сити, Гудзон-Каунти, штат Нью-Джерси', 'Нью-Йорк'],
              ['авеню Пенсильвания Нортвест, 1600', 'Вашингтон'],
              ['остров Пальма Джумейра', 'Дубай']]
    k = choice(spisok)
    return [new_place(k[0]), k[1]]


# подбор коэффициента увеличения карт
def coords(x, y):
    c = 0
    d = 0
    x = float(x)
    y = float(y)
    for i in range(17, -1, -1):
        if x < 180 / 2 ** i:
            d = i + 1
            break
    for j in range(17, -1, -1):
        if y < 360 / 2 ** j:
            c = j + 1
            break
    return abs((c + d) // 2)
