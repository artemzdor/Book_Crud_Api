Book Crud Api

Цель данного проэкта получить практический и теретический опыт.

Стек:
Python3.7
postgresql
aiohttp
asyncpg

Нужно реализовать сервер, предоставляющий HTTP API для редактированияинформации о книгах, которые я прочитал. 
Приложение надо реализовать на языке Python, можно использовать любой фреймворк, кроме Django.
1. Сервер должен предоставлять CRUD API для книг, формат ответов - JSON.
Сущность книга имеет следующие аттрибуты: название, автор, оценка, датапрочтения. 
API должно предоставлять 
4 методаa.
Create - сохранить новую прочитанную книгу.
Read - показать список всех сохраненных книг.
Update - дать возможность изменить оценку книги.
Delete - удалить уже сохраненную книгу (при этом не нужно действительноудалять ее из базы данных - пусть информация о том что она была когда-тодобавлена все еще хранится)

2.Для хранения информации можно использовать любую БД, которую тыпосчитаешь подходящей для решения этой задачи, и которую можно будет потомпотенциально использовать в продакшене.
3.При старте приложения должны выполняться все необходимые операции, чтобыинициализировать БД (например, должны создаваться нужные таблицы, если этонеобходимо).
4.Информация о подключении к БД должна передаваться в приложение черезотдельный файл конфигурации (.json, .yaml, etc)
5.Репозиторий должен содержать Dockerfile, который описывает процесс сборкиобраза приложения.


Инструкци запуска:

клонируем проэкт

git clone https://github.com/artemzdor/Book_Crud_Api.git

заходим в нутрь проэкта
cd ./Book_Crud_Api/docker_src

скачиваем образы приложения и базы
docker-compose pull

запускаем 
docker-compose up

API

методы post:

	/ 	
		возвращает: 200 json -> {"version": "1.0.0", "app": "Book CRUD API"}
		
	/create
	    ожидает: json -> {"name":"n1","author":"a1","assessment":0}
	    возвращает: 
			200 json -> {"id": "1", "successful": true} запись создана 	в случае если запись была удалена то востанавливается и получает новое значине assessment		
			ошибки:
				415 json -> {"massage": "Error decode json", "error": f"Описание ошибки", "successful": False} ошибка декодирования json
				422 json -> {"massage": "Error keys json", "error": 'name, author', "successful": False} ошибка лишние поля или значения не верных типов
	/read
	    возвращает:
			200 json -> [{"id": 1, "name": "n1", "author": "a1", "assessment": 0, "removed": false, "tm_removed": "", "tm_read": 1569318251.927217}] список прочитаных книг
	    
	/update
		ожидает: json -> {"id":1,"assessment":5}
	    возвращает:
			200 json -> {"id": "1", "successful": true} запись обновлена
			ошибки:
				415 json -> {"massage": "Error decode json", "error": f"Описание ошибки", "successful": False} ошибка декодирования json
				422 json -> {"massage": "Error keys json", "error": 'name, author', "successful": False} ошибка лишние поля или значения не верных типов
				460 json -> {"id":"1", "error":"Not found Book","successful":false} ошибка если книга с id 1 не найдена
	    
	/delete
		ожидает: json -> {"id":1}
	    возвращает:
			200 json -> {"id": "1", "successful": true} запись помечена как удаленная. в контролере /read не возвращается
			ошибки:
				415 json -> {"massage": "Error decode json", "error": f"Описание ошибки", "successful": False} ошибка декодирования json
				422 json -> {"massage": "Error keys json", "error": 'name, author', "successful": False} ошибка лишние поля или значения не верных типов
				460 json -> {"id":"1", "error":"Not found Book","successful":false} ошибка если книга с id 1 не найдена

методы get:
	/ 	
		возвращает: 200 json -> {"version": "1.0.0", "app": "Book CRUD API"}
	
	/read
	    возвращает:
			200 json -> [{"id": 1, "name": "n1", "author": "a1", "assessment": 0, "removed": false, "tm_removed": "", "tm_read": 1569318251.927217}] список прочитаных книг


Настройки: 

	environment:
		PATH_CONFIG_JSON=/usr/src/Book_Crud_Api/book_crud_api/config.json
		файл настройки для подключения к postgresql
		{
			"pg_connect": {
				"host": "postgres_db",
				"port": 5432,
				"user": "user_test",
				"password": "example_test",
				"database": "book_crud_api_test"
			}
		}
		SLEEP_START=20 
		время ожидание перед запуском приложения
		postgresql некоторое время подымается
		PYTHONPATH=/usr/src/Book_Crud_Api
		нужно указать корень проэкта для импорта модулей

Сборка
bash ./buld.sh
