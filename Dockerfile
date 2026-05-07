FROM python:3.13-slim

WORKDIR /app

COPY reqirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]