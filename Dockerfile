FROM python:3.10

# Install system dependencies for pycups
RUN apt-get update && apt-get install -y libcups2-dev

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:8000", "your_project.wsgi"]
