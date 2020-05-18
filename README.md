# Декомпозиция
1. Читаем excel файл, сохраняем данные в определенной структуре. Пусть это будет список классов.
Будет базовый класс `BaseCandidate` на тот случай, если мы заходитим расширить функционал, и будет наследник `Candidate` 

    ```
    class BaseCandidate:
        def __init__(self, .... )
            self.position = position.title()
            self.firstname = firstname.title()
            self.lastname = lastname.title()
            self.middlename = '' or middlename.title() # тут может прилететь None
            self.salary = salary  # тут может прилететь None
            self.comment = comment
            self.status = status
            self.fp = ''
    
        @property
        def lastname_firstname():
            return ' '.join([self.lastname, self.firstname])
    ```


2. По ходу написания кода, появится необходимость создания констант,   
эти константы потом вынесем в отдельный файл settings.py

3. Пусть будет структура (пока планирую использовать список) в которой хранятся пути к файлам. 
Для простоты предположим, что если совпадает фамилия и имя.
Для этих целей в предыдущем пункте, в классе используется атрибут `firstname_lastname`,
а для `self.lastname` и `self.firstname` применен метод `title`.
Не будем рассматривать ситуацию, когда есть два кандидата с одинаковыми полями `lastname`, `firstname`.

    *Так как в задании резюме рассортированы по папкам с названиями профессий, то можно,
     для уменьшения вероятности прикладывания в отправку файла однофамильца на будущее заложим привязку профессии 
    к фамаили и имени, этого можно добиться добавив в структуру поле `prof`, туда будем сохранят название папки,
    в которой лежал сам файл. 
    Но этот функционал скорее всего будет реализовываться, если останется время.*

4. Необходимо реализовать функционал добавления(прикрепления) файла к отправке
    * мы храним путь до файла в переменной `fp`
    * как мы отправляем файл? буду использовать `requests`, об этом в отдельно пункте
    * отдельная функция для сравнения(добавления пути файла в атрибут `fp`) по фамилии и имени, что то типа:
        ```for cand in cand_list:
               if cand.lastname_firstname in attachments:
                   cond.fp = attachments['cond.lastname_firstname']
        ```
        `cand_list` - список наших кандидатов, созданных на основе эксель файла   
        `attachments` - список словарей, в котором хранятся пути до файлов, фамилии,
                      в следующем формате:
                       
      ```
        {
            'Иванов Иван': ['filepath','prof'],
            'Петров Петр': ['filepath','prof'],
        }
      ```
      
5. Как мы бегаем по папкам?  
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
вместе с `HOST`, `PORT`, `TOKEN` и тд.  
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

## На сегодня все, не уверен, что буду дополнять этот файл в будущем, так как для MVP этого описания будет достаточно. 