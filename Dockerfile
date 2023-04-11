FROM python

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . /app

WORKDIR /app/api/fitbit

CMD ["python", "loader.py"]
