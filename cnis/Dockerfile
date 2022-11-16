FROM python:latest

WORKDIR user/src/app
RUN pip install --upgrade pip

COPY ./reqs.txt .

RUN pip install -r ./reqs.txt

COPY . .

#CMD ["python", "manage.py", "collectstatic"]
#CMD ["python", "./manage.py", "makemigrations"]
#CMD ["python", "./manage.py", "migrate"]
#CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000"]