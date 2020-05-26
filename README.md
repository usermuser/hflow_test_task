* [Декомпозиция](#decomposition)
<a name="decomposition"></a>
## Декомпозиция
1. Запуск программы будет осуществляться через файл `run.py`.  
Для каждого шага программы создадим отдельную функцию в этом файле. Затем, в функции `run` будем их вызывать.
  
```
def create_canidate():
    """Создаем кандидатов из эксель файла"""
    pass

def upload_resumes():
    """Загружаем файлы с резюме в базу через апи"""
    pass

def add_candidates_to_db():
    """Добавление информации о кандидатах в базу"""
    pass

def add_candidates_to_vacancy():
    """Добавление кандидата на вакансию"""
    pass
```   
  
В задании есть пункт:  
 "Скрипт должен уметь принимать параметры командной строки (токен и путь к папке с базой)."    
 Для этих целей создадим функцию `parse_command_line`. Так как токен и путь к папке с базой это те данные, 
 которые лучше поместить в настройки, то функцию `parse_command_line` будем вызывать из файла настроек `settings.py`.
 В этой функции сделаем проверку корректности переданного пути. 
 Если переданный через коммандную строку путь не корректный, то будем использовать дефолтный путь из настроек.
 Токен можно проверять аналогичным способом, для начала предположим, что если передается токен через коммандную строку,
 то он корректный.
 ```
    FILENAME = 'Тестовая база.xlsx'
    TOKEN, EXCEL_FOLDER = utils.parse_command_line()
    EXCEL_FILE = os.path.join(EXCEL_FOLDER, FILENAME)
```

2. Читаем excel файл, сохраняем данные в определенной структуре. Пусть это будет список классов.
Будет базовый класс `BaseCandidate` на тот случай, если мы заходитим расширить функционал, 
и будет наследник `Candidate` 

    ```
    class BaseCandidate:
        def __init__(self, .... )
            self.position = position.title()
            self.firstname = firstname.title()
            self.lastname = lastname.title()
            self.middlename = '' or middlename.title()    # тут может прилететь None
            self.salary = salary                          # тут может прилететь None
            self.comment = comment
            self.status = status
            self.fp = ''
    
        @property
        def lastname_firstname():
            return ' '.join([self.lastname, self.firstname])
    ```


3. Пусть будет структура (например словарь) в которой хранятся пути к файлам. 
Для простоты предположим, что если совпадает фамилия и имя из эксель файла с фамилией и именем в названии файла,
то файл принадлежит этому кандидату.
Для этих целей в предыдущем пункте, в классе используется атрибут `firstname_lastname`,
а для `self.lastname` и `self.firstname` применен метод `title`.
Не будем рассматривать ситуацию, когда есть два кандидата с одинаковыми полями `lastname`, `firstname`.

    *Так как в задании резюме рассортированы по папкам с названиями профессий, то можно,
     для уменьшения вероятности прикладывания в отправку файла однофамильца на будущее заложим привязку профессии 
    к фамаили и имени, этого можно добиться добавив в структуру поле `prof`, туда будем сохранят название папки,
    в которой лежал сам файл. 
    Но этот функционал скорее всего будет реализовываться, если останется время.*

4. Необходимо реализовать функционал добавления(прикрепления) файла к отправке.

   Создадим отдельный класс `Attachment`, в котором будет метод сохраняющий пути до файлов `_get_attachments()`.
   Также необходимо проверять имена файлов `_prepare_filename()`, так как имена файлов имеют формат `Фамилия Имя`
   либо `Фамилия Имя Отчество`.  
   Также необходим убирать из названий файлов нежелательные символы, 
   для этого используем метод `_remove_undesirable_symbol()`.
   Еще будем отсекать временные файлы при помощи методов `_is_tempfile()` и `_remove_tempfile()`.  
       
   Создадим метод `add_attachment()`, который будет добавлять каждому к кандидату `Candidate()`
   путь до файла в `candidate.fp`.
    
```
    for candidate in candates_list:
       if candidate.lastname_firstname in attachments:
           candidate.filepath = attachments['condidate.lastname_firstname']
```
    `candidate_list` - список наших кандидатов, созданных на основе эксель файла   
    `attachments` - список словарей, в котором хранятся пути до файлов, фамилии,
                    в следующем формате:
                       
```
{
    'Иванов Иван': ['filepath','prof'],
    'Петров Петр': ['filepath','prof'],
}
```
   
   
      
### По подробнее про метод `_get_attachments()`  
По папкам нужно бегать для того чтобы узнать какие файлы с резюме имеются в наличии, а также
необходимо сохранять пути до файлов. Так как в именах файлов присутствуют: имя, фамилия, иногда отчество,
то мы можем это использовать для связывания данных о кандидате, которые мы получили из эксель файла
с данными о том, где лежит файл, который нам нужно прикрепить к отправке.  
Для этих целей можно воспользоваться функцией `os.walk()` стандартной библиотеки. Файлы с резюме поместим в 
папку `cv` в том виде, в котором они были после распаковки архива. Для простоты предположим, что эта папке находится
в одной папке с нашими скриптами.
    ```
        for address, dirs, files in os.walk('cv'):
            # create attachments see previous paragraph
    ```
Подумать о том, что неплохо бы все обернуть в `try except` и отлавливать различные ошибки.
Даже если эта часть программы зафейлилась мы все еще можем отправить то, что мы взяли в эксель файле.
Кстати работу с эксель файлом тоже надо завернуть в `try except`.

6. Отправка запросов при помощи библиотеки requests.  
Реализовать возможность повторной отправки запроса, реализовать так называемую `retry_strategy`. 
Если первый запрос вернул код ошибки из заранее подготовленного списка ошибок (например: 413, 429, 500, 502, 503, 504),
то мы будем пытаться отправить снова через заданное время. Параметры `retry_strategy` будем хранить в `settings.py`, 
вместе с остальными конастантами и настройками.  
    ```
        RETRY_COUNT - количество повторов.
        RETRY_TIMEOUT - сколько ждать ответа при запросе.
        RETRY - флаг повторений (False - не стучимся повторно).
        REPEAT_TIMEOUT - время перед повторным запросом.
        RETRY_CODES - коды при которых повторяем запрос.
    ```

7. Тесты. Тестировать буду при помощи Pytest.  
* Тестируем, что создается наша структура `attachments`, где лежит путь до файла, фамилия, имя, профессия.
Для этого создаем два временных файла (используя библиотеку `tempfile`):   
    файл с резюме в формате pdf/word и эксель файл с данными как в задании.
    
* Тестируем, что наши запросы отправляются. На первый взгляд хочется прямо в тесте поднимать `Flask` сервак,
слушать что присылают и сравнивать. Возможно, лучше обойтись без поднятия сервака, позже решу.

* Тест чтения эксель файла

* Тест работы `retry_strategy`


9. Выполнение запросов
    
    Есть файл с кандидатами `Тестовая база.xslx` с колонками. 
Необходимо добавить кандидатов из этого файла:  
    * в базу
    * и на вакансию на соответствующий этап с комментарием (вакансии уже созданы).

* Добавления кондидатов из этого файла в базу.  
 `POST /account/{account_id}/vacancies`  
  В теле запроса необходимо передать JSON вида:

```
    {
        "position": "Manufacturing Engineer",
        "company": "Tesla",
        "money": "$100k",
        "deadline": "2017-09-03",
        "applicants_to_hire": 2,
        "priority": 1,
        "account_division": 6,
        "coworkers": [1],
        "body": "<p>Some text</p>",
        "requirements": "<p>Another text</p>",
        "conditions": "<p>Different text</p>",
        "hidden": false,
        "state": "OPEN",
        "files": [1, 2, 3]
    }
```

Создадим базовый класс BaseClient. 
Для работы с апи из задачи унаследуемся от базового класса и создадим класс HuntFlowClient.
В этом классе будет метод для `candidate_to_db` для добавления кандидата в базу.
Этот метод будет использовать метод `post` из базового класса.
В методе `post` внедрим `retry_strategy` и будем использовать библиотеку `requests`.


* Добавление кандидата на вакансию на соответствующий этап с комментарием.  
`POST /account/{account_id}/applicants/{applicant_id}/vacancy`  

Действовать будем аналогичным образом, воспользуемся методом post, созданным в базовом классе.
  
   * Желательно успеть прикрутить логирование, правильнее всего было это сделать в самом начале и,  
    по ходу написания программы, логировать важные события. Так как это не было сделано с самого начала,
    буду делать это с этого момента и если не буду забывать. Если останется время после написания тестов,
     займусь логами.
 
    

10. Скрипт должен уметь принимать параметры командной строки (токен и путь к папке с базой).  

Будем использовать `argparse`.  
Пример использования буду смотреть тут: https://pyneng.readthedocs.io/ru/latest/book/12_useful_modules/argparse.html

Токен и путь к папке с базой в случае берем из файла настроек в том случае, 
если в при запуске скрипта эти параметры не заданы. 
Параметры командной строки нужно валидировать перед тем, как пытаться их использовать.
В случае с валидацией токена, не могу сказать точно, скорее всего его валидировать нет необходимости.
Будет понятно валидный он или нет при отправке запроса. Если получим что-то типа "Invalid Token".
В данной задаче не буду затрагивать "Token Expiration", "Token Refreshing".
Касательно пути к папке с базой, то, для валидации, буду использовать `pathlib`   


Создание парсера:  
 * `parser = argparse.ArgumentParser(description='Description')`

Добавление аргументов:  
* `parser.add_argument('-t', action="store", dest="token", help="token")`
* `parser.add_argument('-p', action="store", dest="folder", help="path to database folder")`
* `args = parser.parse_args()`

11. flake8

12. Мой оценочный дедлайн прошел, создал отдельную ветку для когда, который написан после дедлайна.