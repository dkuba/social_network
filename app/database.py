import os

from dotenv import load_dotenv

import psycopg2
from psycopg2 import pool


load_dotenv()


connection_pool = psycopg2.pool.SimpleConnectionPool(
    1, 20,
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    database=os.getenv('DB_NAME')
)


def get_db_connection():
    return connection_pool.getconn()


def put_db_connection(connection):
    connection_pool.putconn(connection)
