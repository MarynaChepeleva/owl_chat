# owl_chat

Чат для курса "Промышленное программирование", РФиКТ 2018 
Авторы: 18_ap_04, 18_ap_23

Для использования чата необходимо иметь Ubuntu и MySQL. 
Чат тестировался на Ubunta 18.04 

Перед запуском:
1) Необходимо установить библиотеку для работы с mysql в python, для этого нужно выполнить в терминале команду:
 pip install mysql-connector==2.1.4
2) Установить MySQL(https://losst.ru/ustanovka-mysql-ubuntu-16-04)
3) Создать в базе данных две таблицы
3.1) chat_user (NAME(varchar 20), PASSWORD(varchar 20))
3.2) post (AUTHOR(varchar 20), TEXT(varchar 100(можно больше)), CREATED_AT(datetime))
4) Скачать или склонировать все файлы в одну папку
5) В файле chat_server.py в строке 7 в скобках создания Databaseconnector прописать юзера и базу данных mysql.

Запуск
1. Запустить сервер(в терминале командой python chat_server.py 'ip address of server' port_num). При запуске без параметров подключается к 127.0.0.1, порт 5050.
2. Запустить любое количество пользователей (в терминале python chat_client.py).

 Unit test:
 Тестируется функция get_hashed_password класса DatabaseConnector, который находится в файле database_methods.py
 Тесты прописаны в док строке и исполняются модулем doctest
 Для запуска в консоли ввести python database_methods.py -v
 
 ООП: database_methods.py, class Database connector выполняет всю работу с базой данных.
 P.S. В Python нет идентификатора private, поэтому поле connector public по умолчанию.
 
 Design Patterns: chat_server.py, строка 65.
 Во всех циклах for в языке программирования python используется паттерн Итератор.
 Так же в этот язык встроен паттерн Генератор, который служит для создания списков и действует быстро и красиво.
 Так же в место return можно использовать в функциях yield, который возвращает генератор.
 Но его использования здесь нет, т.к. не было надобности создавать большие списки.
 
 Дополнительная функциональность:
 1. Многопользовательский режим
 2. Система логирования
 3. Использование базы данных MySQL
 4. Хэширование паролей
 5. Возможность просмотра последних 10 сообщений
 6. Автоматическая регистрация неизвестных ранее пользователей
 7. Просмотр пользователей, которые онлайн
 8. Возможность просмотра своего текущего ника и IP
 9. Автоматическое отключение всех пользователей при отключении сервера
10. Хранение всей переписки всех зарегистрированных пользователей.
