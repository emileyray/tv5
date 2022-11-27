FROM python:3.8.1

RUN python -m pip install pika --upgrade
WORKDIR /app

EXPOSE 8081

COPY . . 

CMD ["python", "send.py"]