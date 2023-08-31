import psycopg2

from config import HOST, DATABASE, USER, PASSWORD
from hh import HeadHunterAPI


class DBManager:
    """ Класс для работы с БД и данными БД"""
    def __init__(self):
        self.host = HOST
        self.database = DATABASE
        self.user = USER
        self.password = PASSWORD
        self.conn = psycopg2.connect(host=self.host,
                                     database=self.database,
                                     user=self.user,
                                     password=self.password)
        self.cur = self.conn.cursor()

    def create_table(self):
        ''' Создает таблицу для хранения данных о вакансии и компаниях'''
        self.cur.execute('''
                            CREATE TABLE vacancies
                            (
                                vacancy_id int PRIMARY KEY,
                                title varchar(100) NOT NULL,
                                url text,
                                salary_from int,
                                salary_to int,
                                description text,
                                company_name varchar(100),
                                company_id int
                            );
                         ''')
        self.conn.commit()

        print("Таблица создана успешно")

    def add_data_to_db(self):
        """ Добавляет данные из HH в таблицу"""
        hh = HeadHunterAPI()
        vacancies = hh.get_vacancies()
        for vacancy in vacancies:
            vacancy_id = vacancy['id']
            title = vacancy['name']
            url = vacancy['alternate_url']
            salary_from = vacancy['salary']['from'] if vacancy['salary'] and vacancy[
                'salary']['from'] else 0
            salary_to = vacancy['salary']['to'] if vacancy['salary'] and vacancy[
                'salary']['to'] else 0
            description = vacancy['snippet']['responsibility']
            company_name = vacancy['employer']['name']
            company_id = vacancy['employer']['id']

            self.cur.execute('INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (vacancy_id, title, url,
                                                                                          salary_from, salary_to,
                                                                                          description, company_name,
                                                                                          company_id))
            self.conn.commit()
        print('Данные добавлены')

    def end_operation(self):
        self.cur.close()
        self.conn.close()

    def get_companies_and_vacancies_count(self):
        '''
        получает список всех компаний и количество вакансий у каждой компании.
        :return:
        '''
        self.cur.execute("SELECT DISTINCT company_name, COUNT(vacancy_id) AS vacancy_count "
                         "FROM vacancies GROUP BY company_name ORDER BY vacancy_count DESC")
        for row in self.cur.fetchall():
            print(f'{row[0]} - {row[1]} вакансий')

    def get_all_vacancies(self):
        '''
        получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        :return:
        '''
        self.cur.execute('SELECT company_name, title, salary_from, salary_to, url '
                         'FROM vacancies '
                         'ORDER BY company_name')
        for row in self.cur.fetchall():
            print(f'{row[0]}\n'
                  f'{row[1]}\n'
                  f'Зарплата от {row[2]} до {row[3]} RUR\n'
                  f'Ссылка на вакансию: {row[4]}',
                  end='\n========================\n')

    def get_avg_salary(self):
        '''
        получает среднюю зарплату по вакансиям.
        :return:
        '''
        self.cur.execute('SELECT AVG(salary_from) AS average_salary '
                         'FROM vacancies '
                         'WHERE salary_from <> 0')
        row = self.cur.fetchall()
        print(f'Средняя зарплата по всем вакансиям: {round(row[0][0])} RUR')

    def get_vacancies_with_higher_salary(self):
        '''
        получает список всех вакансий, у которых зарплата
        выше средней по всем вакансиям.

        :return:
        '''
        self.cur.execute('SELECT title, company_name, salary_from, salary_to, url '
                         'FROM vacancies '
                         'WHERE salary_from > (SELECT AVG(salary_from) AS average_salary '
                         'FROM vacancies WHERE salary_from <> 0);')
        for row in self.cur.fetchall():
            print(f'{row[0]}\n'
                  f'Работа в компании: {row[1]}\n'
                  f'Зарплата от {row[2]} до {row[3]} RUR\n'
                  f'Ссылка на вакансию: {row[4]}',
                  end='\n========================\n')

    def get_vacancies_with_keyword(self, keyword):
        '''
        получает список всех вакансий, в названии которых содержатся
        переданные в метод слова, например python
        :return:
        '''
        self.cur.execute(f"SELECT title, company_name, salary_from, salary_to, url "
                         f"FROM vacancies WHERE title ILIKE '%{keyword}%'")
        for row in self.cur.fetchall():
            print(f'{row[0]}\n'
                  f'Работа в компании: {row[1]}\n'
                  f'Зарплата от {row[2]} до {row[3]} RUR\n'
                  f'Ссылка на вакансию: {row[4]}',
                  end='\n========================\n')
