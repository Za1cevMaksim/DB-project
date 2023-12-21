import psycopg2
import db_insert
import db_create
import db_select


def drop_songs(setup_sql,user,password):
    conn = psycopg2.connect(dbname="musicdb", user=user, password=password, host="127.0.0.1")
    cr = conn.cursor()
    try:
        cr.execute(setup_sql)
        cr.execute("SELECT delete_all_songs()", ())
    finally:
        cr.close()
    conn.commit()

def drop_all(setup_sql,user,password):
    conn = psycopg2.connect(dbname="musicdb", user=user, password=password, host="127.0.0.1")
    cr = conn.cursor()
    try:
        cr.execute(setup_sql)
        cr.execute("SELECT delete_all()", ())
    finally:
        cr.close()
    conn.commit()



def find_user_id(setup_sql,user,password,name):
    conn = psycopg2.connect(dbname="musicdb", user=user, password=password, host="127.0.0.1")
    cr = conn.cursor()
    try:
        cr.execute(setup_sql)
        cr.execute("SELECT * from musicdb.public.find_user_id(%s)",(name,))
        ans = cr.fetchall()
    finally:
        cr.close()
    conn.commit()
    return ans

def find_author_id(setup_sql,user,password,name):
    conn = psycopg2.connect(dbname="musicdb", user=user, password=password, host="127.0.0.1")
    cr = conn.cursor()
    try:
        cr.execute(setup_sql)
        cr.execute("SELECT * from musicdb.public.find_author_id(%s)",(name,))
        ans = cr.fetchall()
    finally:
        cr.close()
    conn.commit()
    return ans

def delete_author(setup_sql,user,password,name):
    conn = psycopg2.connect(dbname="musicdb", user=user, password=password, host="127.0.0.1")
    cr = conn.cursor()
    try:
        cr.execute(setup_sql)
        cr.execute("SELECT delete_author(%s)",(name,))
        ans = cr.fetchall()
    finally:
        cr.close()
    conn.commit()
    return ans

def delete_user(setup_sql,user,password,name):
    conn = psycopg2.connect(dbname="musicdb", user=user, password=password, host="127.0.0.1")
    cr = conn.cursor()
    try:
        cr.execute(setup_sql)
        cr.execute("SELECT delete_user(%s)",(name,))
        ans = cr.fetchall()
    finally:
        cr.close()
    conn.commit()
    return ans

def update_user_theme(setup_sql,user,password,name):
    conn = psycopg2.connect(dbname="musicdb", user=user, password=password, host="127.0.0.1")
    cr = conn.cursor()
    try:
        cr.execute(setup_sql)
        cr.execute("SELECT toggle_theme(%s)",(name,))
    finally:
        cr.close()
    conn.commit()

def add_favorite_song(setup_sql,user,password,username,songname,author):
    conn = psycopg2.connect(dbname="musicdb", user=user, password=password, host="127.0.0.1")
    cr = conn.cursor()
    try:
        cr.execute(setup_sql)
        cr.execute("SELECT add_favorite_song(%s,%s,%s)",(username,songname,author,))
    finally:
        cr.close()
    conn.commit()

def check_favorite(setup_sql,user,password,username,songname,songauthor):
    conn = psycopg2.connect(dbname="musicdb", user=user, password=password, host="127.0.0.1")
    cr = conn.cursor()
    try:
        cr.execute(setup_sql)
        cr.execute("SELECT * from musicdb.public.check_favorite_music(%s,%s,%s)", (username, songname,songauthor,))
        ans = cr.fetchall()
    finally:
        cr.close()
    conn.commit()
    return ans

def return_favorite(setup_sql,user,password,username):
    conn = psycopg2.connect(dbname="musicdb", user=user, password=password, host="127.0.0.1")
    cr = conn.cursor()
    try:
        cr.execute(setup_sql)
        cr.execute("SELECT * from musicdb.public.get_user_favorite_songs(%s)", (username, ))
        ans = cr.fetchall()
    finally:
        cr.close()
    conn.commit()
    return ans

def search_song(setup_sql,user,password,username,text):
    conn = psycopg2.connect(dbname="musicdb", user=user, password=password, host="127.0.0.1")
    cr = conn.cursor()
    try:
        cr.execute(setup_sql)
        cr.execute("SELECT * from musicdb.public.search_songs(%s,%s)", (text,username, ))
        ans = cr.fetchall()
    finally:
        cr.close()
    conn.commit()
    return ans
def download_song(setup_sql,user,password,song,author):
    conn = psycopg2.connect(dbname="musicdb", user=user, password=password, host="127.0.0.1")
    cr = conn.cursor()
    try:
        cr.execute(setup_sql)
        cr.execute("SELECT * from musicdb.public.search_songs_download(%s,%s)", (song,author, ))
        ans = cr.fetchall()
    finally:
        cr.close()
    conn.commit()
    return ans

def is_db_exists(dbname):
    connect = None
    try:
        connect = psycopg2.connect(dbname="postgres", host="127.0.0.1", user="postgres", password="1234")
        connect.autocommit = True
        with connect.cursor() as cur:
            cur.execute("select check_db_exists(%s::varchar)", (dbname,))
            exists = cur.fetchone()
            return exists if exists is None else exists[0]
    finally:
        if connect:
            connect.close()


#create db
#db_create.database_create(setup_sql,user, password, db_name) #database create
#db_create.tables_create(setup_sql,user,password) #create table
#db_insert.use_trigger()


# all insert
#db_insert.insert_users(setup_sql,user, password,'alex','1234') #add user
#db_insert.insert_users(setup_sql, user, password,'maxim', '123456')  # add user
#print(db_select.print_users(setup_sql))
#дальше заполнение
#update_user_theme(setup_sql,user,password,'maxim')
#print(db_select.print_users(setup_sql))
#db_insert.insert_list_author(setup_sql,user, password,'eminem')
#db_insert.insert_list_author(setup_sql,user, password, 'oxxy')
#db_insert.insert_songs(setup_sql,user, password,'123',1,'\\way')
#db_insert.insert_songs(setup_sql,user, password,'235',1,'\\way2')
#db_insert.insert_songs(setup_sql,user, password, '123', 2, '\\way')
#drop from table
#drop_songs(setup_sql)
#db_create.drop_database(setup_sql, db_name) #suddenly doesnt work/dont now whats wrong

#db_insert.insert_list_author(setup_sql,user, password,'Леонтьев')
#db_insert.insert_list_author(setup_sql,user, password, 'PinckFloyd')
#db_insert.insert_songs(setup_sql,user, password, 'Выпьем за любовь', 3, '\\way')
#db_insert.insert_songs(setup_sql,user, password, 'Владимерский централ', 3, '\\way')
#db_insert.insert_songs(setup_sql,user, password, '4536', 4, '\\way')
#db_insert.insert_songs(setup_sql,user, password,'23252635',4,'\\way2')
#add_favorite_song(setup_sql, user, password, 'maxim', 'Выпьем за любовь')
#add_favorite_song(setup_sql, user, password, 'maxim', 'Владимерский централ')
#add_favorite_song(setup_sql, user, password, 'maxim', '23252635')
# all prints
#print(db_select.print_users(setup_sql))
#print(db_select.print_list_author(setup_sql))
#print(db_select.print_songs(setup_sql))
#print(db_select.print_socailmedia(setup_sql))
#print(db_select.print_favorite_songs(setup_sql))

#add_favorite_song(setup_sql,user,password,'maxim','123')

#print(check_favorite(setup_sql,user,password,'maxim','123','eminem'))
#print(check_favorite(setup_sql,user,password,'maxim','123','oxxy'))
#print(check_favorite(setup_sql,user,password,'alex','123','eminem'))

#print(return_favorite(setup_sql,user,password,'maxim'))
#print(db_select.print_favorite_songs(setup_sql))
#add_favorite_song(setup_sql, user, password, 'maxim', '123')
#print(db_select.print_favorite_songs(setup_sql))
#add_favorite_song(setup_sql, user, password, 'maxim', '123')
#print(db_select.print_favorite_songs(setup_sql))
#update status
#update_songs_status(setup_sql,'123',user,password)
#print(db_select.print_songs(setup_sql))

#drop_all(setup_sql,user,password)
#print(find_author_id(setup_sql,user,password,'oxx'))
#delete_author(setup_sql,user,password,'eminem')
#db_insert.update_socialmedia(setup_sql,'oxxy','instagram','vk')
#print(db_select.print_socailmedia(setup_sql))


#print(search_song(setup_sql,user,password,'maxim',''))





