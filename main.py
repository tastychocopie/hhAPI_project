from flask import Flask, render_template, send_from_directory, request
from hh import hhAPI

app = Flask(__name__)
api = hhAPI()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contacts/')
def show_contacts():
    return render_template('contacts.html')


@app.route('/use_api/', methods=['GET', 'POST'])
def use_api():
    if request.method == 'GET':
        # Показываем пустую форму без результатов
        return render_template('hh_api.html', result=None)

    elif request.method == 'POST':
        vacancy_name = request.form.get('vacancy_text', '')
        page_number = request.form.get('page_number', '')
        region = request.form.get('region', '')
        run_type = request.form.get('export_type', '')

        parameters = {
            "text": vacancy_name,
            "page": page_number,
            "area": region
        }

        result = None

        if run_type == 'vacancy_count':
            request_json = api.request_get_json(parameters)
            count = api.count_vacancies(request_json)
            formatted_result = f"Найдено всего вакансий = {count}"

        elif run_type == 'percentage':
            request_json = api.request_get_json(parameters)
            count_vacancies = api.count_vacancies(request_json)
            requirements = api.get_requirements(request_json)
            counter_total = api.count_requirements(requirements)
            result_dict = api.count_requirements_percent(counter_total)
            formatted_result = format_dict_to_html(result_dict, "Проценты требований")

        elif run_type == 'mentions':
            request_json = api.request_get_json(parameters)
            count_vacancies = api.count_vacancies(request_json)
            requirements = api.get_requirements(request_json)
            result_dict = api.count_requirements(requirements)
            formatted_result = format_dict_to_html(result_dict, "Количество упоминаний")

        else:
            formatted_result = None

        # Передаем ВСЕ данные обратно в шаблон
        return render_template('hh_api.html',
                               result=formatted_result,
                               vacancy_text=vacancy_name,
                               page_number=page_number,
                               region=region,
                               export_type=run_type)


def format_dict_to_html(data_dict, title):
    if not data_dict:
        return f"<h4>{title}</h4><p>Нет данных</p>"

    html = f"""
    <h4>{title}</h4>
    <table class="table table-bordered table-hover">
        <thead class="table-light">
            <tr>
                <th>Требование</th>
                <th>Значение</th>
            </tr>
        </thead>
        <tbody>
    """

    for key, value in data_dict.items():
        # Format numbers with commas for thousands
        if isinstance(value, (int, float)):
            formatted_value = f"{value:,}".replace(',', ' ')
        else:
            formatted_value = str(value)

        html += f"""
            <tr>
                <td><strong>{key}</strong></td>
                <td>{formatted_value}</td>
            </tr>
        """

    html += """
        </tbody>
    </table>
    """
    return html

if __name__ == '__main__':
    app.run(debug=True)