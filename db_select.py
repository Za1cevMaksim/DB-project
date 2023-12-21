import psycopg2

def print_users(setup_sql):
    conn = psycopg2.connect(dbname="musicdb", user="postgres", password="1234", host="127.0.0.1")
    cr = conn.cursor()
    try:
        cr.execute(setup_sql)
        cr.execute('SELECT * from musicdb.public.select_users()')
        ans=cr.fetchall()
    finally:
        cr.close()
    conn.commit()
    return ans

def print_list_author(setup_sql):
    conn = psycopg2.connect(dbname="musicdb", user="postgres", password="1234", host="127.0.0.1")
    cr = conn.cursor()
    try:
        cr.execute(setup_sql)
        cr.execute('SELECT * from musicdb.public.select_list_author()')
        ans=cr.fetchall()
    finally:
        cr.close()
    conn.commit()
    return ans



def print_favorite_songs(setup_sql):
    conn = psycopg2.connect(dbname="musicdb", user="postgres", password="1234", host="127.0.0.1")
    cr = conn.cursor()
    try:
        cr.execute(setup_sql)
        cr.execute('SELECT * from musicdb.public.select_favorite_songs()')
        ans=cr.fetchall()
    finally:
        cr.close()
    conn.commit()
    return ans

def print_socailmedia(setup_sql):
    conn = psycopg2.connect(dbname="musicdb", user="postgres", password="1234", host="127.0.0.1")
    cr = conn.cursor()
    try:
        cr.execute(setup_sql)
        cr.execute('SELECT * from musicdb.public.select_socialmedia()')
        ans=cr.fetchall()
    finally:
        cr.close()
    conn.commit()
    return ans

def print_songs(setup_sql):
    conn = psycopg2.connect(dbname="musicdb", user="postgres", password="1234", host="127.0.0.1")
    cr = conn.cursor()
    try:
        cr.execute(setup_sql)
        cr.execute('SELECT * from musicdb.public.select_songs()')
        ans=cr.fetchall()
    finally:
        cr.close()
    conn.commit()
    return ans