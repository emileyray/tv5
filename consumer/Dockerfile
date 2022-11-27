FROM python:3.8.1

RUN python -m pip install pika --upgrade
RUN python -m pip install psycopg2
WORKDIR /app

EXPOSE 8080

COPY . . 

CMD ["python" , "receive.py"]