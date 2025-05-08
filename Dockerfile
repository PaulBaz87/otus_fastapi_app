
# Используем базовый образ Python
FROM python:3.11

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app  

# Копируем файл зависимостей
COPY requirements.txt .

RUN pip install --upgrade pip

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt  

# Копируем весь код проекта в контейнер
# COPY ./app1 /app  
COPY ./app /app 

ENV PYTHONUNBUFFERED=1

# Запуск приложения через Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["python", "/app/database.py"]