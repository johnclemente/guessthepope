FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080
ENV FLASK_ENV=production
ENV SECRET_KEY=change_me_in_production

CMD gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --threads 2