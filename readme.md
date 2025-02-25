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
