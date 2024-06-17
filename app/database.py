import os

from dotenv import load_dotenv

import psycopg2


load_dotenv()

# TODO: восстанавливать соединение при разрыве
connection = psycopg2.connect(
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    database=os.getenv('DB_NAME')
)

connection_slave = psycopg2.connect(
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT_SLAVE'),
    database=os.getenv('DB_NAME')
)


def get_db_connection():
    return connection


def get_db_connection_slave():
    return connection_slave
