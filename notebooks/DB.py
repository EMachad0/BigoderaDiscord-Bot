import psycopg2
from notebooks.config_parser import config


def connect():
    try:
        params = config("postgres")
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return conn


def disconnect():
    if conn is not None:
        conn.close()
        print('Database connection closed.')


conn = connect()

