import psycopg2
import db_insert
import db_create
import db_select





if __name__ == "__main__":
    with open('db_create.sql', 'r') as f:
        setup_sql = f.read()
    db_name="musicdb"
    #db_create.database_create(setup_sql,db_name) #database create
    #db_create.tables_create(setup_sql) #create table
    #db_create.drop_tables(db_name) #suddenly doesnt work/dont now whats wrong

    # all insert
    #db_insert.insert_users(setup_sql,'alex','1234') #add user
    #db_insert.insert_users(setup_sql, 'maxim', '123456')  # add user
    #db_insert.insert_list_author(setup_sql,'eminem')
    #db_insert.insert_list_author(setup_sql, 'oxxy')
    #db_insert.insert_albums(setup_sql,"1","1","1")
    #db_insert.insert_socialmedia(setup_sql,1,'inst','twitter','vkplay')
    #db_insert.insert_socialmedia(setup_sql, 2,  'twitter', 'vkplay')
    #db_insert.insert_songs(setup_sql,'123','1','some text','\\way')
    #db_insert.insert_songs(setup_sql,'235','1','some text')



    # all prints
    print(db_select.print_users(setup_sql))
    print(db_select.print_list_author(setup_sql))
    print(db_select.print_albums(setup_sql))
    print(db_select.print_songs(setup_sql))
    print(db_select.print_socailmedia(setup_sql))




#what need to add
#1) all other from list Lab
#2) refactor all cod (classes and files)
#3) insert_albums (firstly we shoud take name of auther not his id)
#4) insert_socalmedia (maybe it would be better to create lines after before the auther was created from trigger
# and than only update)
#5) add except everywhere in try structure
#6) psycopg2.errors.ForeignKeyViolation: ОШИБКА:  INSERT или UPDATE в таблице "songs" нарушает ограничение внешнего ключа "songs_from_album_fkey"
#:  Ключ (from_album)=(2) отсутствует в таблице "albums". error if add something in songs with albums_name which not in albums





