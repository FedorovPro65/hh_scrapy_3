# Библиотека для анализа данных, представляющая данные в табличном виде называемом DataFrame
# Вся мощь данной библиотеки нам здесь не понадобиться, с ее помощью мы положим
# данные в БД. Можно было бы написать простые insert-ы
import pandas as pd
import numpy as np
import json
import os
import pyodbc
import sys
from dotenv.main import load_dotenv

# Библиотека для работы с СУБД
from sqlalchemy import engine as sql

# Модуль для работы с отображением вывода Jupyter
from IPython import display


def f_truncate(tables_for_truncate: str, connection_string: str):
    ''' Очищает таблицы в БД '''
    # tables_for_truncate = 'dbo.t_vacancies, dbo.t_skills, dbo.t_salary'
    tables = tables_for_truncate.split(',')
    # replace with your SQL Server connection string
    # connection_string = 'Driver={ODBC Driver 17 for SQL Server};Server=NOUTHPFPD22\SS16_2;Database=Test2;Trusted_Connection=yes;'

    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        for table in tables:
            cursor.execute('TRUNCATE TABLE ' + table)

        print(f'f_truncate {tables_for_truncate} end')


def get_connection_string(cur_connect: dict, type_odbc=0):
    # instantiate the variables needed to establish a connection
    server = cur_connect['server']  # 'NOUTHPFPD22\SS16_2'
    database = cur_connect['db']  # 'Test2'
    driver_ = cur_connect['driver']  # 'ODBC Driver 17 for SQL Server'
    username = 'My_username'
    password = 'My_password'

    # define a connection string to establish a connection with the ODBC Driver
    if type_odbc == 0:
        connection_string = f'mssql://@{server}/{database}?driver={driver_}'
    else:
        connection_string = 'Driver={' + driver_ + '};Server=' + server + ';Database=' + database + ';Trusted_Connection=yes;'

    return connection_string





# engine_con = get_connection_string(cur_connect)
# print(engine_con)

# sys.exit("Exit 47")

def write_to_db_sql(cur_connect:str):
    # Создаем списки для столбцов таблицы vacancies
    IDs = []  # Список идентификаторов вакансий
    names = []  # Список наименований вакансий
    descriptions = []  # Список описаний вакансий

    # Создаем списки для столбцов таблицы skills
    skills_vac = []  # Список идентификаторов вакансий
    skills_name = []  # Список названий навыков

    # Создаем списки для столбцов таблицы salary
    salary_vac_id = []  # Список идентификаторов вакансий
    salary_cur = []  # Список валют
    salary_from = []  # от
    salary_to = []  # до
    salary_netto_brutto = []  # netto_brutto (str)

    employers_id = []  # Работодатель
    employers_name = []  # Работодатель
    alternate_url = []  # ссылка на вакансию
    created_at = []  # дата создания вакансии
    schedule = []  # вид занятости

    # В выводе будем отображать прогресс
    # Для этого узнаем общее количество файлов, которые надо обработать
    # Счетчик обработанных файлов установим в ноль
    cnt_docs = len(os.listdir('./docs/vacancies'))
    i = 0

    # Проходимся по всем файлам в папке vacancies
    for fl in os.listdir('./docs/vacancies'):

        # Открываем, читаем и закрываем файл
        f = open('./docs/vacancies/{}'.format(fl), encoding='utf8')
        jsonText = f.read()
        f.close()

        # Текст файла переводим в справочник
        jsonObj = json.loads(jsonText)

        # Заполняем списки для таблиц
        IDs.append(jsonObj['id'])
        names.append(jsonObj['name'])
        descriptions.append(jsonObj['description'])
        alternate_url.append(jsonObj['alternate_url'])
        created_at.append(jsonObj['created_at'][:10])
        sched = jsonObj['schedule']
        schedule.append(sched['name'])
        empl = jsonObj['employer']
        # print(empl)
        employers_id.append(empl['id'])
        employers_name.append(empl['name'])

        # Т.к. зарплаты хранятся в виде словаря, то проходимся по нему циклом
        print(jsonObj['salary'])
        print(type(jsonObj['salary']))
        salary_vac_id.append(jsonObj['id'])
        if type(jsonObj['salary']).__name__ == 'NoneType':
            print('--- NULL---')
            salary_to.append(np.nan)
            salary_cur.append(np.nan)
            salary_from.append(np.nan)
            salary_netto_brutto.append(np.nan)
        else:
            # salary_cur.append(sal['currency'])
            cur = jsonObj['salary']
            salary_from.append(cur['from'])
            salary_to.append(cur['to'])
            salary_cur.append(cur['currency'])
            if cur['gross']:
                salary_netto_brutto.append('gross')
            else:
                salary_netto_brutto.append('netto')

        # Т.к. навыки хранятся в виде массива, то проходимся по нему циклом
        for skl in jsonObj['key_skills']:
            skills_vac.append(jsonObj['id'])
            skills_name.append(skl['name'])

        # Увеличиваем счетчик обработанных файлов на 1, очищаем вывод ячейки и выводим прогресс
        i += 1
        display.clear_output(wait=True)
        display.display('Готово {} из {}'.format(i, cnt_docs))

    # Создадим соединение с БД
    engine_con = get_connection_string(cur_connect)
    engine = sql.create_engine(engine_con)
    conn = engine.connect()

    # Создаем пандосовский датафрейм, который затем сохраняем в БД в таблицу vacancies
    df = pd.DataFrame({'id': IDs, 'name': names, 'description': descriptions,
                       'employer_id': employers_id, 'employer_name': employers_name,
                       'alternate_url': alternate_url, 'created_date': created_at,
                       'schedule': schedule
                       })
    df.to_sql('t_vacancies', conn, schema='dbo', if_exists='append', index=False)

    # Тоже самое, но для таблицы skills
    df = pd.DataFrame({'vacancy': skills_vac, 'skill': skills_name})
    df.to_sql('t_skills', conn, schema='dbo', if_exists='append', index=False)

    # Тоже самое, но для таблицы skills
    df = pd.DataFrame({'vac_id': salary_vac_id, 'salary_cur': salary_cur, 'salary_from': salary_from
                          , 'salary_to': salary_to, 'Netto_brutto': salary_netto_brutto})
    df.to_sql('t_salary', conn, schema='dbo', if_exists='append', index=False)

    # Закрываем соединение с БД
    conn.close()

    # Выводим сообщение об окончании программы
    display.clear_output(wait=True)
    display.display('Вакансии загружены в БД')

def truncate_and_write_to_db_sql():
    # Save_Pages_To_Files(2,'NAME:SQL разработчик')
    # Читаем переменные из env
    load_dotenv()

    cur_driver = os.environ['DRIVER']
    cur_db = os.environ['DATABASE']
    cur_server = os.environ['SERVER']
    cur_connect = {'driver': cur_driver, 'db': cur_db, 'server': cur_server}
    connection_string = get_connection_string(cur_connect, 1)  # os.environ['CONNECTION_ODBC_STR']
    print(connection_string)

    f_truncate('dbo.t_vacancies, dbo.t_skills, dbo.t_salary',
               connection_string)

    write_to_db_sql(cur_connect)
if __name__ == '__main__':
    # # Save_Pages_To_Files(2,'NAME:SQL разработчик')
    # # Читаем переменные из env
    # load_dotenv()
    #
    # cur_driver = os.environ['DRIVER']
    # cur_db = os.environ['DATABASE']
    # cur_server = os.environ['SERVER']
    # cur_connect = {'driver': cur_driver, 'db': cur_db, 'server': cur_server}
    # connection_string = get_connection_string(cur_connect, 1)  # os.environ['CONNECTION_ODBC_STR']
    # print(connection_string)
    #
    # f_truncate('dbo.t_vacancies, dbo.t_skills, dbo.t_salary',
    #            connection_string)
    #
    # write_to_db_sql(cur_connect)
    truncate_and_write_to_db_sql()
