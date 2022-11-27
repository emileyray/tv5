#!/usr/bin/env python
import pika
import sys
import os
import psycopg2


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    conn = psycopg2.connect(
        database="postgresdb", user='postgresadmin', password='admin123', host='localhost', port='5432'
    )

    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS type1")
    cursor.execute("DROP TABLE IF EXISTS type2")

    sql = '''CREATE TABLE type1(
        ID  SERIAL PRIMARY KEY,
        ENTRY CHAR(5) NOT NULL,
    )'''
    cursor.execute(sql)

    sql = '''CREATE TABLE type2(
        ID  SERIAL PRIMARY KEY,
        ENTRY CHAR(5) NOT NULL,
    )'''
    cursor.execute(sql)
    conn.commit()

    def callback(ch, method, properties, body):
        postgres_insert_query = """ INSERT INTO %s (ENTRY) VALUES (%s)"""
        record_to_insert = (body[0:5], body[6:])
        cursor.execute(postgres_insert_query, record_to_insert)
        conn.commit()

        print(" [x] Received %r" % body)

    channel.basic_consume(
        queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
