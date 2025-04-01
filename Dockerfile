FROM python:3.10-slim

WORKDIR /app

COPY registration_tracker/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY registration_tracker/app /app

RUN python3 database_creation.py

CMD [ "streamlit", "run", "home.py"]