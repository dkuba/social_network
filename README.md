### Заготовка для социальной сети


- клонируйте репозиторий

```commandline
git clone git@github.com:dkuba/social_network.git
```

- создайте .env файл рядом c .env.example
- поднимите сервисы
```commandline
docker-compose up -d --build
```

По-умолчанию сервис будет на порту 8000, а база на порту 5432.

### Примеры запросов

#### Создать пользователя

Запрос:
```curl
curl --location 'localhost:8000/v1/users' \
--header 'Content-Type: application/json' \
--data-raw '{"username": "Foo",
"password": "123",
"email": "foo@ya.ru",
"first_name": "Vova",
"last_name": "Vovin",
"date_of_birth": "2018-01-10",
"user_gender": "муж",
"city": "Москва",
"interests": "everythings"
}'
```

Ответ:

```commandline
{
    "user_id": "b922b380-3f38-4897-b0c5-b3ca7a5e7ac4"
}
```

#### Логин

Запрос:
```curl
curl --location 'localhost:8000/v1/login' \
--header 'Content-Type: application/json' \
--data '{"username": "Foo",
"password": "123"}'
```

Ответ:
```commandline
{
    "session_token": "Wg1tyNq27xFdnTiZ-PZmnF93UY5Vsdj6waO8b3mrGNo"
}
```

#### Информация о пользователе по id

Запрос:

```curl
curl --location 'localhost:8000/v1/users/b922b380-3f38-4897-b0c5-b3ca7a5e7ac4' \
--header 'Authorization: Bearer Wg1tyNq27xFdnTiZ-PZmnF93UY5Vsdj6waO8b3mrGNo'
```

Ответ:
```commandline
{
    "username": "Foo",
    "password": "123",
    "email": "foo@ya.ru",
    "first_name": "Vova",
    "last_name": "Vovin",
    "date_of_birth": "2018-01-10",
    "user_gender": "муж",
    "city": "Москва",
    "interests": null,
    "id": "b922b380-3f38-4897-b0c5-b3ca7a5e7ac4"
}
```
