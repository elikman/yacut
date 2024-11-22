# YaCut - Укротитель Ссылок

## Описание
**YaCut** - cервис укорачивания ссылок, который заменяет длинную ссылку на короткую (до 16 символов).
Вариант сокращения может быть задан как самим пользователем, так и сгенерирован автоматически сервисом.
Все сокращения уникальны. Реализован Web-интерфейс для пользователей и REST API.

### Стек технологий

![](https://img.shields.io/badge/Python-3.9-black?style=flat&logo=python) 
![](https://img.shields.io/badge/Flask-2.0.2-black?style=flat&logo=flask)
![](https://img.shields.io/badge/SQLAlchemy-1.4.29-black?style=flat&logo=sqlalchemy)

#### Установка

***1.Клонировать репозиторий и перейти в него в командной строке: ***

```bash
https://github.com/elikman/yacut.git
```

```bash
cd yacut
```

***2. Cоздать и активировать виртуальное окружение: ***

```bash
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

* Запуск приложения

    ```
    flask run
    ```


***3. Установить зависимости из файла requirements.txt: ***

```bash
python3 -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

#### Основные эндпоинты
/ - Web-интерфейс для генерации короткой ссылки

/<short_id>/ - Web-интерфейс для переадресации на исходную ссылку

/api/id/ - POST-запрос к API для генерации короткой ссылки

/api/id/<short_id>/ - GET-запрос для получения исходной ссылки из короткой

#### Примеры запросов

**GET** `.../api/id/{short_id}/`
*200*
```
{
  "url": "string"
}
```
*404*
```
{
  "message": "Указанный id не найден"
}
```


**POST** `.../api/id/`
```
{
  "url": "string",
  "custom_id": "string"
}
```
*201*
```
{
  "url": "string",
  "short_link": "string"
}
```
*400*
```
{
  "message": "Отсутствует тело запроса"
}
```

#### Автор

Набиев Эльтадж