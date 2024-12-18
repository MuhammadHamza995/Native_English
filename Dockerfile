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

# Step 7: Install uWSGI
RUN pip install uwsgi

# Step 8: Copy the Django project files into the container
COPY . /app/

# Accept SECRET_KEY as a build argument
ARG SECRET_KEY

ARG ALLOWED_HOSTS

# Set SECRET_KEY as an environment variable
ENV SECRET_KEY=${SECRET_KEY}

ENV ALLOWED_HOSTS=${ALLOWED_HOSTS}

# Step 9: Collect static files (if needed for your project)
RUN python manage.py collectstatic --noinput

# Step 10: Expose the port for the backend
EXPOSE 8000

# Step 11: Command to run uWSGI
CMD ["uwsgi", "--ini", "app.ini"]