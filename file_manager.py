import os
import json

class fileManager:

    JSON_FILES_DIR_NAME = "json файлы"

    def createFolder(self):
        os.makedirs(self.JSON_FILES_DIR_NAME, exist_ok=True)

    def generateJsonPercent(self, title, information):
        self.createFolder()  # создаем директорию

        # information[0] - parameters
        # information[1] - result
        # information[2] - vacancies_total
        parameters = information[0]
        result = information[1]
        vacancies_total = information[2]

        requirements = []
        for skill_name, percent in result.items():
            requirement = {
                'name': skill_name,
                'percent': percent
            }
            requirements.append(requirement)

        result_data = [{
            'key_words': parameters.get('text', ''),
            'vacancies_total_items': vacancies_total,
            'requirements': requirements
        }]

        filename = f"{title}.json"
        filepath = os.path.join(self.JSON_FILES_DIR_NAME, filename)

        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(result_data, file, ensure_ascii=False, indent=4)

        print(f"создали JSON файл: {filepath}")

    def generateJsonCount(self, title, information):
        self.createFolder()  # создаем директорию

        # information[0] - parameters
        # information[1] - result
        # information[2] - vacancies_total
        parameters = information[0]
        result = information[1]
        vacancies_total = information[2]

        requirements = []
        for skill_name, count in result.items():
            requirement = {
                'name': skill_name,
                'count': count
            }
            requirements.append(requirement)

        result_data = [{
            'key_words': parameters.get('text', ''),
            'vacancies_total_items': vacancies_total,
            'requirements': requirements
        }]

        filename = f"{title}.json"
        filepath = os.path.join(self.JSON_FILES_DIR_NAME, filename)

        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(result_data, file, ensure_ascii=False, indent=4)

        print(f"создали JSON файл: {filepath}")