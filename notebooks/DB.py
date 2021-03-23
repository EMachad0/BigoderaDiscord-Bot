import os
import psycopg2


def connect():
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(os.environ["DATABASE_URL"])
        print("Connected")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return conn


def disconnect():
    if conn is not None:
        conn.close()
        print('Database connection closed.')


conn = connect()

