FROM python:3.10-slim-bullseye

ENV PYTHONPATH "${PYTHONPATH}:/app"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY extractors extractors

WORKDIR extractors/fitbit

CMD ["python", "extractor.py"]
