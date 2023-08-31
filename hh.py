import requests


class HeadHunterAPI:
    employers: tuple[dict] | list[dict] = (
        {'company': 'ООО Фармамед', 'id': 1461426},
        {'company': 'ВЕРТЕКС', 'id': 73441},
        {'company': 'АО «ФАРМПРОЕКТ»', 'id': 10234407},
        {'company': 'ООО «НТФФ «ПОЛИСАН»', 'id': 4548},
        {'company': 'SOLOPHARM', 'id': 1228187},
        {'company': 'ООО Фармакор Продакшн', 'id': 19752},
        {'company': 'НАО Северная звезда', 'id': 1443941},
        {'company': 'АО Активный Компонент', 'id': 1273771},
        {'company': 'АО Витал', 'id': 654889},
        {'company': 'НПК Технолог', 'id': 10233968},
        {'company': 'Самсон - Мед', 'id': 719463},
        {'company': 'ГК Фармасинтез', 'id': 829326},
        {'company': 'БИОКАД, биотехнологическая компания', 'id': 389},
        {'company': 'Мирролла', 'id': 2452730},
        {'company': 'Герофарм', 'id': 25629},
        {'company': 'АО Р-Фарм', 'id': 8121}
    )
    url = 'https://api.hh.ru/vacancies'

    def __init__(self):
        self.vacancies: list = []

    def get_vacancies(self):
        """
        Получает вакансии компаний из списка
        """

        i = 0
        while i <= len(self.employers) - 1:
            params: dict = {
                'archived': False,
                'employer_id': self.employers[i]['id'],
                'per_page': 100
                }
            response = requests.get(self.url, params=params).json()['items']
            self.vacancies.extend(response)
            i += 1
        return self.vacancies
