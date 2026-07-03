FROM python:3.11-slim

WORKDIR /app

# Устанавливаем Chrome для работы в headless-режиме
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Команда для запуска тестов
CMD ["pytest", "--headless", "--alluredir=allure-results", "--cov=pages", "--cov=config", "--cov-report=html", "--cov-report=term"]