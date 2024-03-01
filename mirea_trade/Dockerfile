# Базовый образ Python
FROM python:3.9

# Устанавливаем рабочую директорию в контейнере
WORKDIR /mirea_trade
# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем зависимости
RUN pip install --upgrade pip
COPY ./requirements.txt /mirea_trade/requirements.txt
RUN pip install -r requirements.txt

# Копируем проект
COPY . /mirea_trade/