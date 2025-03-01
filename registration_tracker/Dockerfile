FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app /app

RUN python database_creation.py

CMD [ "streamlit", "run", "app.py"]