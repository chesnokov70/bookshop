#!/bin/sh

echo "Жду PostgreSQL..."
until pg_isready -h postgres -p 5432 -U bookshop; do
  sleep 1
done

echo "PostgreSQL доступен. Запуск приложения..."
exec python run.py
