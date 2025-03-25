FROM python:3.10-slim

WORKDIR /app

COPY registration_tracker/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY registration_tracker/app /app

CMD [ "streamlit", "run", "home.py"]