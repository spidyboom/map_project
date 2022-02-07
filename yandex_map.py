from io import BytesIO
from typing import Optional, Tuple

import requests
from PIL import Image


class YandexMap():

    def __init__(self,
                 l: str,
                 ll: Tuple[float, float],
                 key: Optional[str] = None,
                 spn: Optional[float] = None,
                 z: Optional[int] = None,
                 size: Optional[Tuple[int, int]] = None,
                 scale: Optional[Tuple[float, float]] = None,
                 pt: Optional[str] = None,
                 pl: Optional[str] = None,
                 lang="ru_RU"):
        """Api для YandexStatic

        Полная документация - https://yandex.ru/dev/maps/staticapi/doc/1.x/dg/concepts/input_params.html

        Args:
            l: Перечень слоев, определяющих тип карты: map (схема), sat (спутник) и sat,skl (гибрид).
            ll: Долгота и широта центра карты в градусах
            key: Api ключ для коммерческой версии
            spn: Протяженность области показа карты по долготе и широте (в градусах)
            z: Уровень масштабирования карты (0-17)
            size: Ширина и высота запрашиваемого изображения карты (в пикселах)
            scale: Коэффициент увеличения объектов на карте. Может принимать дробное значение от 1.0 до 4.0.
            pt: Содержит описание одной или нескольких меток, которые требуется отобразить на карте.
            pl: Содержит набор описаний геометрических фигур (ломаных и многоугольников), которые требуется отобразить на карте. 
            lang: Язык, по умолчанию ru_RU
        """

        self._l = l
        self._ll = ll
        self._key = key
        self._spn = spn
        self._z = z
        self._size = size
        self._scale = scale
        self._pt = pt
        self._pl = pl
        self._lang = lang

        self.api_server = "http://static-maps.yandex.ru/1.x/"

    def get_params(self) -> dict:
        res = {}
        if self._l:
            res['l'] = self._l
        if self._ll:
            res['ll'] = f'{float(self._ll[0])},{float(self._ll[1])}'
        if self._key:
            res['key'] = self._key
        if self._spn:
            res['spn'] = self._spn
        if self._z:
            res['z'] = self._z
        if self._size:
            res['size'] = self._size
        if self._scale:
            res['scale'] = self._scale
        if self._pt:
            res['pt'] = self._pt
        if self._pl:
            res['pl'] = self._pl
        if self._lang:
            res['lang'] = self._lang

        return res

    def get(self) -> Image.Image:
        response = requests.get(self.api_server, params=self.get_params())
        img_in_bytes = BytesIO(response.content)
        img = Image.open(img_in_bytes)
        return img

    def change_l(self, new_l: str) -> Image.Image:
        self._l = new_l
        return self.get()

    def delta_change_ll(self, delta_ll: Tuple[float, float]) -> Image.Image:
        self._ll = (self._ll[0] + delta_ll[0], self._ll[1] + delta_ll[1])
        return self.get()


if __name__ == "__main__":
    api = YandexMap('map', (37.620070, 55.753630))
    api.get()
    api.delta_change_ll((10, 10)).show()

