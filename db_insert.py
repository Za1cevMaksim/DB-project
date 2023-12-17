import psycopg2

def insert_users(setup_sql,login,password):
    conn = psycopg2.connect(dbname="musicdb", user="postgres", password="1234", host="127.0.0.1")
    cr = conn.cursor()
    try:
        cr.execute(setup_sql)
        cr.execute("SELECT insert_user(%s, %s)", (login, password,))
    finally:
        cr.close()
    conn.commit()

def insert_list_author(setup_sql,name):
    conn = psycopg2.connect(dbname="musicdb", user="postgres", password="1234", host="127.0.0.1")
    cr = conn.cursor()
    try:
        cr.execute(setup_sql)
        cr.execute("SELECT insert_list_author(%s)", (name,))
    finally:
        cr.close()
    conn.commit()

#need to rework function(should take name_author insted author_id)
def insert_albums(setup_sql,albums_name,year,author_id):
    conn = psycopg2.connect(dbname="musicdb", user="postgres", password="1234", host="127.0.0.1")
    cr = conn.cursor()
    try:
        cr.execute(setup_sql)
        cr.execute("SELECT insert_albums(%s, %s, %s)", (albums_name,year,author_id,))
    finally:
        cr.close()
    conn.commit()

def insert_socialmedia(setup_sql,author_id,*args):
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


    conn = psycopg2.connect(dbname="musicdb", user="postgres", password="1234", host="127.0.0.1")
    cr = conn.cursor()
    try:
        cr.execute(setup_sql)
        cr.execute("SELECT insert_socialmedia(%s, %s, %s, %s)", (author_id,instagram,twitter,any_other,))
    finally:
        cr.close()
    conn.commit()

def insert_songs(setup_sql,songs_name,from_album,*args):
    link='NULL'
    text_txt='NULL'
    for i in args:
        if '\\' in i:
            link=i
        else:
            text_txt=i

    conn = psycopg2.connect(dbname="musicdb", user="postgres", password="1234", host="127.0.0.1")
    cr = conn.cursor()
    try:
        cr.execute(setup_sql)
        cr.execute("SELECT insert_songs(%s,%s,%s,%s,%s)", (songs_name,link,text_txt,0, from_album,))
    finally:
        cr.close()
    conn.commit()