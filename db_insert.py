import psycopg2

def insert_users(setup_sql,user,password,login,password_users):
    conn = psycopg2.connect(dbname="musicdb", user=user, password=password, host="127.0.0.1")
    cr = conn.cursor()
    try:
        cr.execute(setup_sql)
        cr.execute("SELECT insert_user(%s, %s)", (login, password_users,))
    finally:
        cr.close()
    conn.commit()

def insert_list_author(setup_sql,user,password,name):
    conn = psycopg2.connect(dbname="musicdb", user=user, password=password, host="127.0.0.1")
    cr = conn.cursor()
    try:
        cr.execute(setup_sql)
        cr.execute("SELECT insert_list_author(%s)", (name,))
    finally:
        cr.close()
    conn.commit()


def update_socialmedia(setup_sql,user,password,author_name,*args):
    instagram='NULL'
    twitter='NULL'
    any_other='NULL'
    for i in args:
        if 'inst' in i:
            instagram=i
        elif 'twit' in i:
            twitter=i
        else:
            any_other=i

    conn = psycopg2.connect(dbname="musicdb", user=user, password=password, host="127.0.0.1")
    cr = conn.cursor()
    try:
        cr.execute(setup_sql)
        cr.execute("SELECT update_socialmedia(%s, %s, %s, %s)", (author_name,instagram,twitter,any_other,))
    finally:
        cr.close()
    conn.commit()

def insert_songs(setup_sql,user,password,songs_name,author_id,link):
    link='NULL'

    conn = psycopg2.connect(dbname="musicdb", user=user, password=password, host="127.0.0.1")
    cr = conn.cursor()
    try:
        cr.execute(setup_sql)
        cr.execute("SELECT insert_songs(%s,%s,%s)", (songs_name,link,author_id,))
    finally:
        cr.close()
    conn.commit()

def use_trigger():
    with open('trigger.sql', 'r') as f:
        trigger = f.read()
    conn = psycopg2.connect(dbname="musicdb", user="postgres", password="1234", host="127.0.0.1")
    cr = conn.cursor()
    cr.execute(trigger)
    conn.commit()