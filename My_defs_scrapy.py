# Библиотека для работы с HTTP-запросами. Будем использовать ее для обращения к API HH
import requests

# Пакет для удобной работы с данными в формате json
import json

# Модуль для работы со значением времени
import time

# Модуль для работы с операционной системой. Будем использовать для работы с файлами
import os, shutil


def getPage(page=0, str_find='NAME:аналитик'):
    """
   Создаем метод для получения страницы со списком вакансий.
   Аргументы:
       page - Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница
   """

    # Справочник для параметров GET-запроса
    params = {
        'text': str_find,  # Текст фильтра. В имени должно быть слово "SQL разработчик"
        'area': 1,  # Поиск осуществляется по вакансиям города Москва
        'page': page,  # Индекс страницы поиска на HH
        'per_page': 40  # Кол-во вакансий на 1 странице
    }

    req = requests.get('https://api.hh.ru/vacancies', params)  # Посылаем запрос к API
    data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
    req.close()
    return data

def Save_Pages_To_Files(pages:int, str_find='NAME:аналитик' ):
    # Очищаем целевые папки для записывания новых файлов с данными
    myfolder = './docs/pagination'
    cleaner_folder(myfolder)
    myfolder = './docs/vacancies'
    cleaner_folder(myfolder)
    # Считываем первые 2000 вакансий
    for page in range(0,pages):
       print(page)
       # Преобразуем текст ответа запроса в справочник Python
       jsObj = json.loads(getPage(page, str_find))

       # Сохраняем файлы в папку {путь до текущего документа со скриптом}\docs\pagination
       # Определяем количество файлов в папке для сохранения документа с ответом запроса
       # Полученное значение используем для формирования имени документа
       nextFileName = './docs/pagination/{}.json'.format(len(os.listdir('./docs/pagination')))

       # Создаем новый документ, записываем в него ответ запроса, после закрываем
       f = open(nextFileName, mode='w', encoding='utf8')
       f.write(json.dumps(jsObj, ensure_ascii=False))
       f.close()
       print(jsObj['pages'])
       # Проверка на последнюю страницу, если вакансий меньше 2000
       if (jsObj['pages'] - page) <= 1:
          break

       # Необязательная задержка, но чтобы не нагружать сервисы hh, оставим. 5 сек мы может подождать
       time.sleep(10.25)

    print(f'Страницы поиска "{str_find}" собраны.')

def create_vacancies_files(count_vac_max=3):
    # Получаем перечень ранее созданных файлов со списком вакансий и проходимся по нему в цикле
    count_vac = 0
    for fl in os.listdir('./docs/pagination'):

        # Открываем файл, читаем его содержимое, закрываем файл
        f = open('./docs/pagination/{}'.format(fl), encoding='utf8')
        jsonText = f.read()
        print(f.name)
        f.close()

        # Преобразуем полученный текст в объект справочника
        jsonObj = json.loads(jsonText)

        # Получаем и проходимся по непосредственно списку вакансий
        for v in jsonObj['items']:
            count_vac += 1
            if count_vac > count_vac_max:
                break
            # Обращаемся к API и получаем детальную информацию по конкретной вакансии

            req = requests.get(v['url'])
            data = req.content.decode()
            req.close()

            # Создаем файл в формате json с идентификатором вакансии в качестве названия
            # Записываем в него ответ запроса и закрываем файл
            fileName = './docs/vacancies/{}.json'.format(v['id'])
            f = open(fileName, mode='w', encoding='utf8')
            f.write(data)
            f.close()

            time.sleep(5.25)

    print('Вакансии собраны')


def cleaner_folder(folder: str):
    ''' Очищает папку от файлов и папок в ней '''
    i = 0
    j = 0
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                i += 1
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                j += 1
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    print(f'Удалено {i} файлов и {j} папок')

if __name__ == '__main__':
    Save_Pages_To_Files(5,'NAME:SQL разработчик')
    create_vacancies_files(200)

