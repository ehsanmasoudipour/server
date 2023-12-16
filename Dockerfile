# Use an official Python runtime as a parent image
FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install poetry
RUN pip install poetry

# Set the working directory to /usr/src/app
WORKDIR /usr/src/app

# Copy only the dependencies file to leverage Docker cache
COPY poetry.lock pyproject.toml /usr/src/app/

# Install project dependencies
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Expose port 8000 for the Django application
EXPOSE 8000

# Run django-admin commands when the container starts
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
