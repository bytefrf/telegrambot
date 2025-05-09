# Базовый образ
FROM python:3.10-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода бота
COPY bot.py .

# Команда для запуска бота
CMD ["python", "bot.py"]
