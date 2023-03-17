# coding:utf-8

import requests

import pandas as pd

def get_file_of_tg(id, token):
    zap = f'''https://api.telegram.org/bot{token}/getFile?file_id={id}'''
    response = requests.get(zap).json()["result"]["file_path"]
    dls = f'https://api.telegram.org/file/bot{token}/{response}'
    resp = requests.get(dls)
    output = open('dow.xlsx', 'wb')
    output.write(resp.content)
    output.close()


def check_file_of_tg():
    a = [['ID', 'ФИО', 'Должность(1-админ, 0-клиент', 'ID TG', 'UserName'],
         ['ID Категории', 'Название категории', 'Путь к файлу картинки'],
         ['Сообщение', 'Дата отправления'],
         ['Вопрос', 'Ответ'],
         ['Название', 'Описание']]
    flag = True
    for sheet in range(5):
        df = pd.read_excel(io='dow.xlsx', sheet_name=sheet)
        if ''.join(df.head(0).columns.values) != ''.join(a[sheet]):
            flag = False
            break
    return flag


print(check_file_of_tg())
def geocode(address):
    # Собираем запрос для геокодера.
    geocoder_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={address}&format=json".format(**locals())
    # Выполняем запрос.
    response = requests.get(geocoder_request)

    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()
    else:
        raise RuntimeError(
            """Ошибка выполнения запроса:
            {request}
            Http статус: {status} ({reason})""".format(
                request=geocoder_request, status=response.status_code, reason=response.reason))

    # Получаем первый топоним из ответа геокодера.
    # Согласно описанию ответа он находится по следующему пути:
    features = json_response["response"]["GeoObjectCollection"]["featureMember"]
    return features[0]["GeoObject"] if features else None


# Получаем координаты объекта по его адресу.
def get_coordinates(address):
    toponym = geocode(address)
    if not toponym:
        return None, None

    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Широта, преобразованная в плавающее число:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    return float(toponym_longitude), float(toponym_lattitude)


# Получаем параметры объекта для рисования карты вокруг него.
def get_ll_span(address):
    toponym = geocode(address)
    if not toponym:
        return None, None

    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    print(toponym)
    # Долгота и Широта :
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    # Собираем координаты в параметр ll
    ll = ",".join([toponym_longitude, toponym_lattitude])

    # Рамка вокруг объекта:
    envelope = toponym["boundedBy"]["Envelope"]

    # левая, нижняя, правая и верхняя границы из координат углов:
    l, b = envelope["lowerCorner"].split(" ")
    r, t = envelope["upperCorner"].split(" ")

    # Вычисляем полуразмеры по вертикали и горизонтали
    dx = abs(float(l) - float(r)) / 0.8
    dy = abs(float(t) - float(b)) / 0.8

    # Собираем размеры в параметр span
    span = "{dx},{dy}".format(**locals())

    return ll, span


# Находим ближайшие к заданной точке объекты заданного типа.
def get_nearest_object(point, kind):
    geocoder_request_template = "http://geocode-maps.yandex.ru/1.x/?geocode={ll}&kind={kind}&format=json"
    ll = "{0},{1}".format(point[0], point[1])

    # Выполняем запрос к геокодеру, анализируем ответ.
    geocoder_request = geocoder_request_template.format(**locals())
    response = requests.get(geocoder_request)
    raise RuntimeError(
        """Ошибка выполнения запроса:
        {geocoder_request}
        Http статус: {status} ({reason})""".format(
            request=geocoder_request, status=response.status_code, reason=response.reason))

    # Преобразуем ответ в json-объект
    json_response = response.json()

    # Получаем первый топоним из ответа геокодера.
    features = json_response["response"]["GeoObjectCollection"]["featureMember"]
    return features[0]["GeoObject"]["name"] if features else None


if __name__ == '__main__':
    ll, spn = get_ll_span("Арзамас, Парковая 14А")
    ll1, spn1 = get_ll_span("Арзамас, Зеленая 138")
    print(ll, spn)
    if ll and spn and ll1 and spn1:
        point = "{ll},pm2vvm~{ll1},pmntl".format(ll=ll, ll1=ll1)
        static_api_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&spn=0.5,0.5&l=map&pt={point}".format(**locals())
        print(static_api_request)
