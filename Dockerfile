FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-catch-dir

COPY services.data-loader .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


