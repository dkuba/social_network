import os

from dotenv import load_dotenv

import psycopg2

load_dotenv()


def get_conn():
    return psycopg2.connect(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME')
    )


def get_slave_conn():
    return psycopg2.connect(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST_SLAVE'),
        port=os.getenv('DB_PORT_SLAVE'),
        database=os.getenv('DB_NAME')
    )


master_conn = get_conn()
replica_conn = get_slave_conn()


def get_db_connection():
    global master_conn
    try:
        cursor = master_conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
    except psycopg2.OperationalError:
        master_conn = get_conn()

    return master_conn


def get_db_connection_slave():
    global replica_conn
    try:
        cursor = replica_conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
    except psycopg2.OperationalError:
        replica_conn = get_slave_conn()

    return replica_conn
