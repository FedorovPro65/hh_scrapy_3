# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# pip install requests
# pip install pandas
# pip install pyodbc
# pip install sqlalchemy
# pip install IPython
# pip install python-dotenv

from My_defs_write_to_sqldb import truncate_and_write_to_db_sql
from My_defs_scrapy import Save_Pages_To_Files, create_vacancies_files

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Save_Pages_To_Files(2,'NAME:SQL разработчик')
    create_vacancies_files(200)
    truncate_and_write_to_db_sql()

