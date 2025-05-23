# bookstore

## Create table
```
CREATE TABLE book (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100) NOT NULL,
    price FLOAT NOT NULL
);
```

## Endpoints
- GET /books: Получить список всех книг
- POST /books: Создать новую книгу
- GET /books/<id>: Получить информацию о конкретной книге
- PUT /books/<id>: Обновить информацию о книге
- DELETE /books/<id>: Удалить книгу

## Exapmle requests
```
# Получить инфо
curl -X GET http://localhost:5000/books
curl -X GET http://localhost:5000/books/1

# Создать запись о книге
curl -X POST http://localhost:5000/books \
  -H "Content-Type: application/json" \
  -d '{"title":"Новая книга","author":"Автор","price":19.99}'

# Отредактировать запись
curl -X PUT http://localhost:5000/books/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Обновленное название","author":"Новый автор","price":24.99}'

# Удалить
curl -X DELETE http://localhost:5000/books/1
```
##----------------------------------------------------------
docker exec -it bookshop-app-postgres-1 psql -U bookshop -d bookshopdb

bookshopdb=# CREATE TABLE book (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100) NOT NULL,
    price FLOAT NOT NULL
);
bookshopdb=# \d book

curl -X POST http://localhost/books \
  -H "Content-Type: application/json" \
  -d '{"title":"Новая книга","author":"Автор","price":19.99}'
{"author":"\u0410\u0432\u0442\u043e\u0440","id":1,"price":19.99,"title":"\u041d\u043e\u0432\u0430\u044f \u043a\u043d\u0438\u0433\u0430"}

curl http://localhost/books

curl http://localhost/books | jq

docker exec -it opt-nginx-1 curl http://bookshop_api:5000/books