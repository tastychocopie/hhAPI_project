# получать необходимую информацию из hh.ru
# используется hh API
# на данный предусмотрен следующий функционал:
## 1: подсчет открытых вакансий в целом
## 2: подсчет процента, насколько часто конкретное требование требуется в вакансии
## 3: подсчет количества упоминаний требований

import pprint
import json
from hh import hhAPI
from file_manager import fileManager

# таким образом появляется api.hh.ru
api = hhAPI()

# импортируем менеджера файлов
myFileManager = fileManager()

while True:
    print('1. Подсчет вакансий')
    print('2. Подсчет процента')
    print('3. Подсчет упоминаний')
    print('4. Сведения текущих параметров')
    print('5. Обновление параметров')
    print('6. Выход')

    # выбор пользователя
    choice = input('Выберите пункт: ')

    match choice:
        case '1':
            print('производим подсчет вакансий суммарно...')
            parameters = api.initialize_base_parameters()
            request_json = api.request_get_json(parameters)
            vacancy_counter = api.count_vacancies(request_json)
            pprint.pprint(vacancy_counter)

        case '2':
            print('производим подсчет процента требований относительно к вакансиям')
            parameters = api.initialize_base_parameters()
            request_json = api.request_get_json(parameters)
            vacancy_counter = api.count_vacancies(request_json)
            requirements = api.get_requirements(request_json)
            counter_total = api.count_requirements(requirements)
            percentages_total = api.count_requirements_percent(counter_total)
            pprint.pprint(percentages_total)
            print('сохранить результат в виде JSON файла?')
            print('1. да')
            print('2. нет')
            sub_choice = input('ваш выбор: ')
            match sub_choice:
                case '1':
                    myFileManager.generateJsonPercent('percent_data', [parameters, percentages_total, vacancy_counter])
                    continue
                case '2':
                    continue
                case _:
                    print('выбран неверный пункт, возвращаемся в главное меню')
                    continue

        case '3':
            print('производим подсчет упоминаний требований...')
            parameters = api.initialize_base_parameters()
            request_json = api.request_get_json(parameters)
            vacancy_counter = api.count_vacancies(request_json)
            requirements = api.get_requirements(request_json)
            counter_total = api.count_requirements(requirements)
            pprint.pprint(counter_total)
            print('сохранить результат в виде JSON файла?')
            print('1. да')
            print('2. нет')
            sub_choice = input('ваш выбор: ')
            match sub_choice:
                case '1':
                    myFileManager.generateJsonCount('counter_data', [parameters, counter_total, vacancy_counter])
                    continue
                case '2':
                    continue
                case _:
                    print('выбран неверный пункт, возвращаемся в главное меню')
                    continue

        case '4':
            current_parameters = api.initialize_base_parameters()
            pprint.pprint(current_parameters)

        case '5':
            print('Введите параметры в формате JSON, на пример {"text": "QA developer"}')
            custom_parameters = input('JSON: ')
            try:
                params_dict = json.loads(custom_parameters)
                new_parameters = api.update_parameters(**params_dict)
                print('Обновленные параметры: \n')
                pprint.pprint(new_parameters)
            except Exception as e:
                print(f"Ошибка: {e}")

        case '6':
            print('выход из системы')
            break
        case _:
            print('выберите верный пункт')