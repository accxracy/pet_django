FROM python:3.13.5-slim


SHELL ["/bin/bash", "-c"]


RUN apt update && apt install -y \
    libcrypt1 \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app


RUN pip install --upgrade pip


COPY requirements.txt .

RUN pip install -r requirements.txt


COPY . .


RUN python manage.py collectstatic --noinput

EXPOSE 8000


CMD ["gunicorn", "pet.wsgi:application", "--bind", "0.0.0.0:8000"]
