from db_manager import DBManager

dbm = DBManager()
# Работа с БД
# Создать таблицу vacancies, добавить данные в таблицу
# dbm.create_table()
# dbm.add_data_to_db()
# dbm.end_operation()

# Работа с данными

# получить список всех компаний и количество вакансий у каждой компании
# dbm.get_companies_and_vacancies_count()

# получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
# dbm.get_all_vacancies()

# получить среднюю зарплату по всем вакансиям
# dbm.get_avg_salary()

# получить список всех вакансий, у которых зарплата выше средней по всем вакансиям
# dbm.get_vacancies_with_higher_salary()

# получить список всех вакансий, в названии которых содержатся переданные в метод слова, например python
# dbm.get_vacancies_with_keyword('слово для поиска')
