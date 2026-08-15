FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY evaluator ./evaluator
COPY dataset ./dataset
COPY reports ./reports

ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "evaluator.compare"]