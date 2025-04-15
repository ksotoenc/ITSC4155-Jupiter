FROM python:3.10-slim

WORKDIR /app

COPY registration_tracker/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY registration_tracker/app /app

RUN python database_creation.py

# Add an entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# ENTRYPOINT ["/entrypoint.sh"]
CMD [ "streamlit", "run", "home.py"]