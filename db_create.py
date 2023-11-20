import psycopg2

def database_create():
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="1234", host="127.0.0.1")
    cursor = conn.cursor()

    conn.autocommit = True
    # команда для создания базы данных metanit
    sql = "CREATE DATABASE MusicBD"

    # выполняем код sql
    cursor.execute(sql)

    cursor.close()
    conn.close()

    print("db create")


def database_setup():
    conn = psycopg2.connect(dbname="musicbd", user="postgres", password="1234", host="127.0.0.1")
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS List_of_Authors (id SERIAL PRIMARY KEY, name VARCHAR(50))")
    conn.commit()
    cursor.close()

    conn.close()

    print("first table create")