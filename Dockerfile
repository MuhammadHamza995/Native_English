# Step 1: Use Python 3.12 image
FROM python:3.12

# Step 2: Install dependencies required for building uwsgi
RUN apt-get update && \
    apt-get install -y build-essential python3-dev libpq-dev

# Step 3: Set environment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8

# Step 4: Set working directory inside the container
WORKDIR /app

# Step 5: Copy the requirements file into the container
COPY requirements.txt /app/

# Step 6: Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install redis celery

# Step 7: Install uWSGI
RUN pip install uwsgi

# Step 8: Copy the Django project files into the container
COPY . /app/

# Accept SECRET_KEY as a build argument
ARG SECRET_KEY

ARG ALLOWED_HOSTS

ARG DATABASE_URL

# Set SECRET_KEY as an environment variable
ENV SECRET_KEY=${SECRET_KEY}

ENV ALLOWED_HOSTS=${ALLOWED_HOSTS}

ENV DATABASE_URL=${DATABASE_URL}

ENV EMAIL_HOST = ${EMAIL_HOST}

ENV EMAIL_PORT = ${EMAIL_PORT}

ENV EMAIL_USE_TLS = ${EMAIL_USE_TLS}

ENV INFO_EMAIL_HOST_USER = ${INFO_EMAIL_HOST_USER}

ENV INFO_EMAIL_HOST_PASSWORD = ${INFO_EMAIL_HOST_PASSWORD}

ENV NOTIFY_EMAIL_HOST_USER = ${NOTIFY_EMAIL_HOST_USER}

ENV NOTIFY_EMAIL_HOST_PASSWORD = ${NOTIFY_EMAIL_HOST_PASSWORD}

ENV CELERY_BROKER_URL = ${CELERY_BROKER_URL}

ENV CELERY_RESULT_BACKEND = ${CELERY_RESULT_BACKEND}
# Step 9: Collect static files (if needed for your project)
RUN python manage.py collectstatic --noinput

# Step 10: Expose the port for the backend
EXPOSE 8000

# Step 11: Command to run uWSGI
CMD ["sh", "-c", "python manage.py migrate && uwsgi --ini app.ini"]