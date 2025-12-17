# импорт необходимых библиотек, pprint для красивого вывода, а requests для работы с REST API
import requests
from datetime import datetime

class hhAPI:

    """
    Базовые свойства
    """

    # основной домейн, выбран hh
    BASE_URL = 'https://api.hh.ru/' # хард-кодим hh api, чтобы только он использовался
    VACANCIES_URL = f"{BASE_URL}vacancies" # ссылка на вакансии

    """
        text - значение поиска в vacancies
        page - страница
        area - регион
    """
    BASE_PARAMETERS = {
        'text': 'python developer',
        'page': 1,
        'area': 1
    }

    PARAMETERS_CACHE = None

    """
    Базовые методы класса
    """

    def initialize_base_parameters(self):
        if self.PARAMETERS_CACHE is None:
            self.PARAMETERS_CACHE = self.BASE_PARAMETERS

        return self.PARAMETERS_CACHE

    def get_default_parameters(self):
        if self.PARAMETERS_CACHE is None:
            self.PARAMETERS_CACHE = self.BASE_PARAMETERS
        return self.BASE_PARAMETERS

    # создание параметров для get() запроса
    def update_parameters(self, **additional_params ):
        updated_params = {**self.BASE_PARAMETERS, **additional_params}
        self.PARAMETERS_CACHE = updated_params
        return updated_params

    # получение get() запроса в виде json
    def request_get_json(self, parameters):
        result = requests.get(self.VACANCIES_URL, parameters).json()
        return result

    """
    Методы для подсчетов + методы получения вакансий детально:
    published_at - дата размещения вакансии
    item['employer'].name - организация
    name - название вакансии
    """

    # метод получения деталей
    def get_details(self, result):
        details_list =[]
        vacancies = result['items']
        for vacancy in vacancies:
            details = {}
            published_date = vacancy['published_at']
            # форматируем дату
            try:
                dt = datetime.strptime(published_date, '%Y-%m-%dT%H:%M:%S%z')
                details['published_at'] = dt.strftime('%d.%m.%Y %H:%M')
            except:
                details['published_at'] = published_date

            organization = vacancy['employer']['name']
            details['employer'] = organization
            vacancy_name = vacancy['name']
            details['name'] = vacancy_name
            details_list.append(details)

        print(details_list)
        return details_list

    def count_vacancies(self, result):
        vacancies = result['items']
        vacancies_total = len(vacancies)
        return vacancies_total

    # для count_requirements
    def get_requirements(self, result):
        # получение вакансий в целом
        vacancies = result['items']

        requirements = []

        # запуск цикла, который будет пробегать по каждому item в items и находить requirement в snippet
        for item in vacancies:
            snippet = item['snippet']
            get_requirements = snippet['requirement']
            requirements.append(get_requirements)

        return requirements

    def count_requirements(self, requirements):
        # будем искать по требованию, т.е. python, django, flask, sqlalchemy
        counters = {
            'python': 0,
            'django': 0,
            'flask': 0,
            'sqlalchemy': 0
        }
        for requirement in requirements:
            # приводим в lowerCase для более точного поиска
            requirement_lower = requirement.lower()

            if 'python' in requirement_lower:
                counters['python'] += 1
            elif 'django' in requirement_lower:
                counters['django'] += 1
            elif 'flask' in requirement_lower:
                counters['flask'] += 1
            elif 'sqlalchemy' in requirement_lower:
                counters['sqlalchemy'] += 1

        return counters

    def count_requirements_percent(self, counters):
        # подсчет значений всех ключей из counters
        total = sum(counters.values())
        percentages = {}
        for key, value in counters.items():
            percentage = (value / total) * 100
            percentages[key] = round(percentage, 1) # округляем
        return percentages