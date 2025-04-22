FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

RUN touch votes.db \
 && chmod 666 votes.db

# Expose the port EB will route to
EXPOSE 5000

# Default command: run with Gunicorn
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:5000", "app:app"]