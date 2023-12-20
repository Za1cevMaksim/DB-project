import psycopg2
import db_insert
import db_create
import db_select


def drop_songs(setup_sql):
    conn = psycopg2.connect(dbname="musicdb", user="postgres", password="1234", host="127.0.0.1")
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

def update_songs_status(setup_sql,song_name,users,password):
    conn = psycopg2.connect(dbname="musicdb", user=users, password=password, host="127.0.0.1")
    cr = conn.cursor()
    try:
        cr.execute(setup_sql)
        cr.execute("SELECT update_value_songs(%s)", (song_name,))
    finally:
        cr.close()
    conn.commit()

def update_user_right(setup_sql):
    conn = psycopg2.connect(dbname="musicdb", user="postgres", password="1234", host="127.0.0.1")
    cr = conn.cursor()
    try:
        cr.execute(setup_sql)
        cr.execute("SELECT update_func_owner()",())
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


if __name__ == "__main__":
    with open('db_create.sql', 'r') as f:
        setup_sql = f.read()
    user='users'
    password='123456'
    db_name="musicdb"
    db_create.database_create(setup_sql,user, password, db_name) #database create
    db_create.tables_create(setup_sql,user,password) #create table
    #db_create.drop_database(setup_sql, db_name) #suddenly doesnt work/dont now whats wrong
    use_trigger()

    #print(db_select.print_list_author(setup_sql))
    # all insert
    #db_insert.insert_users(setup_sql,'alex','1234') #add user
    #db_insert.insert_users(setup_sql, 'maxim', '123456')  # add user
    #db_insert.insert_list_author(setup_sql,'eminem')
    db_insert.insert_list_author(setup_sql, 'oxxy')
    #db_insert.insert_albums(setup_sql,"1","1","3")
    #db_insert.insert_socialmedia(setup_sql,3,'inst','twitter','vkplay')
    #db_insert.insert_socialmedia(setup_sql, 4,  'twitter', 'vkplay')
    #db_insert.insert_songs(setup_sql,'123','1','some text','\\way')
    #db_insert.insert_songs(setup_sql,'235','1','some text')

    #drop from table
    #drop_songs(setup_sql)

    #check trigger
    #db_insert.insert_list_author(setup_sql, 'satyr')

    # all prints
    #print(db_select.print_users(setup_sql))
    print(db_select.print_list_author(setup_sql))
    #print(db_select.print_albums(setup_sql))
    #print(db_select.print_songs(setup_sql))
    #print(db_select.print_socailmedia(setup_sql))


    #update status
    #update_user_right(setup_sql)
    #update_songs_status(setup_sql,'123',user,password)
    #print(db_select.print_songs(setup_sql))
    #drop_all(setup_sql,user,password)




#what need to add
#1) all other from list Lab
#2) refactor all cod (classes and files)
#3) insert_albums (firstly we shoud take name of auther not his id)
#4) insert_socalmedia (maybe it would be better to create lines after before the auther was created from trigger
# and than only update)
#5) add except everywhere in try structure
#6) psycopg2.errors.ForeignKeyViolation: ОШИБКА:  INSERT или UPDATE в таблице "songs" нарушает ограничение внешнего ключа "songs_from_album_fkey"
#:  Ключ (from_album)=(2) отсутствует в таблице "albums". error if add something in songs with albums_name which not in albums





