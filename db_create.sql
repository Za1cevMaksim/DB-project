CREATE EXTENSION IF NOT EXISTS dblink;

-- function to create database
DROP FUNCTION IF EXISTS create_db(text, text, text);
CREATE OR REPLACE FUNCTION create_db(username VARCHAR(255), password VARCHAR(255), dbname text)
RETURNS VOID AS
    $$
    BEGIN
        IF EXISTS (SELECT datname FROM pg_database WHERE datname = dbname) THEN
             RAISE NOTICE 'Database already exists';
        ELSE
             PERFORM dblink_exec('user=postgres password=1234 dbname= ' || current_database(),
                    'CREATE DATABASE ' || dbname);

            PERFORM dblink_exec(format('user=postgres password=1234 dbname=%I',  current_database()),
                format('CREATE USER %I WITH SUPERUSER PASSWORD %L', username, password));


            PERFORM dblink_exec(format('user=postgres password=1234 dbname=%I',  current_database()),
                format('GRANT ALL PRIVILEGES ON DATABASE %I TO %I', dbname, username));


            PERFORM dblink_exec(format('user=postgres password=1234 dbname=%I',  dbname),
                format('GRANT ALL PRIVILEGES ON SCHEMA public TO %I', username));


            PERFORM dblink_exec(format('user=postgres password=1234 dbname=%I', dbname),'CREATE EXTENSION IF NOT EXISTS dblink');
        END IF;
    END;
    $$
LANGUAGE plpgsql;




-- function to create all tables
DROP FUNCTION IF EXISTS create_tables();
CREATE OR REPLACE FUNCTION create_tables()
RETURNS VOID AS
    $$
    BEGIN
        CREATE TABLE IF NOT EXISTS users(
                                    id SERIAL PRIMARY KEY,
                                    username varchar(20) NOT NULL UNIQUE,
                                    password varchar(30) NOT NULL,
                                    theme text default 'Dark'
                                );

        CREATE TABLE IF NOT EXISTS list_author(
                                    id SERIAL PRIMARY KEY,
                                    name varchar(30) NOT NULL UNIQUE
                                );


        CREATE TABLE IF NOT EXISTS socialmedia(
                                    author_id SERIAL PRIMARY KEY ,
                                    FOREIGN KEY (author_id) REFERENCES list_author (id) ON DELETE CASCADE,
                                    instagram text,
                                    twitter text,
                                    any_other text
                                );

        CREATE TABLE IF NOT EXISTS songs(
            id SERIAL PRIMARY KEY,
            songs_name varchar(40) NOT NULL,
            link text,
            from_author integer NOT NULL,
            FOREIGN KEY (from_author) REFERENCES list_author (id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS favorite_songs(
                                    id SERIAL PRIMARY KEY,
                                    song_id integer NOT NULL,
                                    user_id integer NOT NULL,
                                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                                    FOREIGN KEY (song_id) REFERENCES songs (id) ON DELETE CASCADE
        );
    END
    $$
LANGUAGE plpgsql;

--full drop db doesnt work now--
DROP FUNCTION IF EXISTS drop_database(text);
CREATE OR REPLACE FUNCTION drop_database(dbname text)
  RETURNS VOID LANGUAGE sql AS
    $func$
    --ALTER DATABASE musicdb CONNECTION LIMIT 0;
    SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'musicdb';
    SELECT dblink_exec('user=postgres password=1234 dbname = postgres'  , 'DROP DATABASE ' || quote_ident(dbname))
    $func$;


--insert into users tables--
DROP FUNCTION IF EXISTS insert_user(VARCHAR(20), VARCHAR(30));
CREATE OR REPLACE FUNCTION insert_user(user_name VARCHAR(20), pass_word VARCHAR(30))
    RETURNS VOID AS
    $$
    BEGIN
        INSERT INTO musicdb.public.users (username, password) VALUES (user_name, pass_word);
    END;
    $$
LANGUAGE plpgsql;


--insert into users list_author--
DROP FUNCTION IF EXISTS insert_list_author(VARCHAR(30));
CREATE OR REPLACE FUNCTION insert_list_author(names VARCHAR(30))
    RETURNS VOID AS
    $$
    BEGIN
        INSERT INTO musicdb.public.list_author (name) VALUES (names);
    END;
    $$
LANGUAGE plpgsql;


--insert into users favourite_songs--
DROP FUNCTION IF EXISTS insert_favourite_songs(VARCHAR(40),integer);
CREATE OR REPLACE FUNCTION insert_favourite_songs(song_names VARCHAR(40), user_ids integer)
    RETURNS VOID AS
    $$
    BEGIN
        INSERT INTO musicdb.public.favorite_songs (song_name,user_id) VALUES (song_names,user_ids);
    END;
    $$
LANGUAGE plpgsql;

--insert into users social_media--
DROP FUNCTION IF EXISTS insert_socialmedia(integer, text,text,text);
CREATE OR REPLACE FUNCTION insert_socialmedia(ids integer, instagrams text, twitters text, any_others text)
    RETURNS VOID AS
    $$
    BEGIN
        INSERT INTO musicdb.public.socialmedia (author_id,instagram,twitter,any_other) VALUES (ids,instagrams,twitters,any_others);
    END;
    $$
LANGUAGE plpgsql;

--insert into users songs--
DROP FUNCTION IF EXISTS insert_songs(varchar(40),text,integer);
CREATE OR REPLACE FUNCTION insert_songs(song_names varchar(40), links text, from_authors integer)
    RETURNS VOID AS
    $$
    BEGIN
        INSERT INTO musicdb.public.songs (songs_name,link,from_author) VALUES (song_names,links,from_authors);
    END;
    $$
LANGUAGE plpgsql;


--print for user tables--
DROP FUNCTION IF EXISTS select_users();
CREATE FUNCTION select_users()
    RETURNS TABLE(username VARCHAR, password VARCHAR, theme text) AS
    $$
    BEGIN
        RETURN QUERY
        SELECT musicdb.public.users.username, musicdb.public.users.password, musicdb.public.users.theme FROM musicdb.public.users;
    END
	$$
LANGUAGE plpgsql;

--print for list_auther tables--
DROP FUNCTION IF EXISTS select_list_author();
CREATE FUNCTION select_list_author()
    RETURNS TABLE(name VARCHAR) AS
    $$
    BEGIN
        RETURN QUERY
        SELECT musicdb.public.list_author.name FROM musicdb.public.list_author;
    END
	$$
LANGUAGE plpgsql;


--print for favorite_songs tables--
DROP FUNCTION IF EXISTS select_favorite_songs();
CREATE FUNCTION select_favorite_songs()
    RETURNS TABLE(song_id integer, user_id integer) AS
    $$
    BEGIN
        RETURN QUERY
        SELECT musicdb.public.favorite_songs.song_id, musicdb.public.favorite_songs.user_id FROM musicdb.public.favorite_songs;
    END
	$$
LANGUAGE plpgsql;

--print for socialmedia tables--
DROP FUNCTION IF EXISTS select_socialmedia();
CREATE FUNCTION select_socialmedia()
    RETURNS TABLE(author_id integer, instagram text, twitter text) AS
    $$
    BEGIN
        RETURN QUERY
        SELECT musicdb.public.socialmedia.author_id, musicdb.public.socialmedia.instagram, musicdb.public.socialmedia.twitter FROM musicdb.public.socialmedia;
    END
	$$
LANGUAGE plpgsql;

--print for songs tables--
DROP FUNCTION IF EXISTS select_songs();
CREATE FUNCTION select_songs()
    RETURNS TABLE(id integer, songs_name varchar(40), link text, author integer) AS
    $$
    BEGIN
        RETURN QUERY
        SELECT * FROM musicdb.public.songs;
    END
	$$
LANGUAGE plpgsql;


--drop all from favorite_songs--
DROP FUNCTION IF EXISTS delete_all_favorite_songs();
CREATE OR REPLACE FUNCTION delete_all_favorite_songs()
RETURNS VOID AS $$
BEGIN
    DELETE FROM musicdb.public.favorite_songs;
END
$$ LANGUAGE plpgsql;


--drop all from songs--
DROP FUNCTION IF EXISTS delete_all_songs();
CREATE OR REPLACE FUNCTION delete_all_songs()
RETURNS VOID AS $$
BEGIN
    DELETE FROM musicdb.public.songs;
END
$$ LANGUAGE plpgsql;

--delete all from all tables--
DROP FUNCTION IF EXISTS delete_all();
CREATE OR REPLACE FUNCTION delete_all()
RETURNS VOID AS $$
BEGIN
    DELETE FROM musicdb.public.favorite_songs;
    DELETE FROM musicdb.public.list_author;
    DELETE FROM musicdb.public.socialmedia;
    DELETE FROM musicdb.public.songs;
    DELETE FROM musicdb.public.users;
END
$$ LANGUAGE plpgsql;

--find id author with name--
DROP FUNCTION IF EXISTS find_author_id(varchar(30));
CREATE OR REPLACE FUNCTION find_author_id(names varchar(30) )
RETURNS integer AS $$
DECLARE
    author_id INTEGER;
BEGIN
    SELECT musicdb.public.list_author.id INTO author_id from musicdb.public.list_author
    WHERE musicdb.public.list_author.name=names;

    RETURN author_id;
END
$$ LANGUAGE plpgsql;


--find id user with name--
DROP FUNCTION IF EXISTS find_user_id(varchar(20));
CREATE OR REPLACE FUNCTION find_user_id(names varchar(20))
RETURNS integer AS $$
DECLARE
    user_id INTEGER;
BEGIN
    SELECT musicdb.public.users.id INTO user_id from musicdb.public.users
    WHERE musicdb.public.users.username=names;

    RETURN user_id;
END
$$ LANGUAGE plpgsql;

--delete author from list_author--
DROP FUNCTION IF EXISTS delete_author(varchar(30));
CREATE OR REPLACE FUNCTION delete_author(author_names VARCHAR(30))
RETURNS VOID AS $$
BEGIN
    DELETE FROM musicdb.public.list_author
    WHERE musicdb.public.list_author.name = author_names;
END;
$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS delete_user(varchar(20));
CREATE OR REPLACE FUNCTION delete_user(usernames VARCHAR(20))
RETURNS VOID AS $$
BEGIN
    DELETE FROM musicdb.public.users
    WHERE musicdb.public.users.username = usernames;
END;
$$ LANGUAGE plpgsql;


--change users theme--
DROP FUNCTION IF EXISTS toggle_theme(varchar(20));
CREATE OR REPLACE FUNCTION toggle_theme(user_names VARCHAR(20))
RETURNS VOID AS $$
BEGIN
    UPDATE musicdb.public.users
    SET theme = CASE WHEN musicdb.public.users.theme = 'Light' THEN 'Dark' ELSE 'Light' END
    WHERE musicdb.public.users.username = user_names;
END
$$ LANGUAGE plpgsql;



DROP FUNCTION IF EXISTS add_favorite_song(varchar(20),VARCHAR(30));
CREATE OR REPLACE FUNCTION add_favorite_song(usernames VARCHAR(20), song VARCHAR(30))
RETURNS VOID AS $$
DECLARE
    user_ids INTEGER;
    song_ids INTEGER;
BEGIN
    SELECT musicdb.public.users.id INTO user_ids
    FROM musicdb.public.users
    WHERE musicdb.public.users.username = usernames;

    SELECT  musicdb.public.songs.id INTO song_ids
    FROM musicdb.public.songs
    WHERE musicdb.public.songs.songs_name = song;

     IF EXISTS (SELECT 1 FROM musicdb.public.favorite_songs WHERE musicdb.public.favorite_songs.user_id = user_ids AND musicdb.public.favorite_songs.song_id = song_ids) THEN
        DELETE FROM musicdb.public.favorite_songs
        WHERE musicdb.public.favorite_songs.user_id = user_ids AND musicdb.public.favorite_songs.song_id = song_ids;
    ELSE
        INSERT INTO musicdb.public.favorite_songs (user_id, song_id)
        VALUES (user_ids, song_ids);
    END IF;
END
$$ LANGUAGE plpgsql;

--update socialmedia--
DROP FUNCTION IF EXISTS update_socialmedia(varchar(30),text,text,text);
CREATE OR REPLACE FUNCTION update_socialmedia(author_name VARCHAR(30), instagrams text, twitters text, any_others text)
RETURNS VOID AS $$
DECLARE
    author_ids INTEGER;
BEGIN

    SELECT musicdb.public.list_author.id INTO author_ids
    FROM musicdb.public.list_author
    WHERE musicdb.public.list_author.name = author_name;


    UPDATE musicdb.public.socialmedia
    SET
        instagram = instagrams,
        twitter = twitters,
        any_other = any_others
    WHERE author_id = author_ids;
END;
$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS check_favorite_music(varchar(20),VARCHAR(40),VARCHAR(30));
CREATE OR REPLACE FUNCTION check_favorite_music(usernames VARCHAR(20), song_names VARCHAR(40), song_author VARCHAR(30))
RETURNS BOOLEAN AS $$
DECLARE
    author_id INTEGER;
    user_ids INTEGER;
    song_ids INTEGER;
    is_favorite BOOLEAN;
BEGIN

    SELECT  musicdb.public.list_author.id INTO author_id
    FROM  musicdb.public.list_author
    WHERE musicdb.public.list_author.name=song_author;


    SELECT musicdb.public.users.id INTO user_ids
    FROM musicdb.public.users
    WHERE musicdb.public.users.username = usernames;


    SELECT musicdb.public.songs.id INTO song_ids
    FROM  musicdb.public.songs
    WHERE musicdb.public.songs.songs_name = song_names AND musicdb.public.songs.from_author= author_id;

    is_favorite := EXISTS (
        SELECT 1
        FROM musicdb.public.favorite_songs
        WHERE musicdb.public.favorite_songs.user_id= user_ids AND musicdb.public.favorite_songs.song_id = song_ids
    );

    RETURN is_favorite;
END;
$$ LANGUAGE plpgsql;



DROP FUNCTION IF EXISTS get_user_favorite_songs(VARCHAR(20));
CREATE OR REPLACE FUNCTION get_user_favorite_songs(user_name VARCHAR(20))
RETURNS TABLE (song_name VARCHAR, author_name VARCHAR) AS $$
DECLARE
    user_ids INTEGER;
BEGIN

    SELECT musicdb.public.users.id INTO user_ids
    FROM musicdb.public.users
    WHERE musicdb.public.users.username = user_name;

    RETURN QUERY
    SELECT
        musicdb.public.songs.songs_name,
        musicdb.public.list_author.name
    FROM
        musicdb.public.favorite_songs
    JOIN
        musicdb.public.songs ON musicdb.public.favorite_songs.song_id = musicdb.public.songs.id
    JOIN
        musicdb.public.list_author ON musicdb.public.songs.from_author = musicdb.public.list_author.id
    WHERE
        musicdb.public.favorite_songs.user_id = user_ids;
END;
$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS search_songs(VARCHAR(20),varchar(20));
CREATE OR REPLACE FUNCTION search_songs(text VARCHAR(20),usernames varchar(20) )
RETURNS TABLE (id integer, song_name VARCHAR, song_author VARCHAR,status boolean) AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM list_author WHERE name = text) THEN
        RETURN QUERY
        SELECT
            musicdb.public.songs.id,
            musicdb.public.songs.songs_name,
            musicdb.public.list_author.name,
            check_favorite_music(usernames, songs_name, musicdb.public.list_author.name)
        FROM
            musicdb.public.songs
        JOIN
            musicdb.public.list_author ON musicdb.public.songs.from_author = musicdb.public.list_author.id
        WHERE
            musicdb.public.songs.from_author = (SELECT musicdb.public.list_author.id FROM musicdb.public.list_author WHERE musicdb.public.list_author.name = text);
    ELSE
        RETURN QUERY
        SELECT
            musicdb.public.songs.id,
            musicdb.public.songs.songs_name,
            musicdb.public.list_author.name,
            check_favorite_music(usernames, songs_name, musicdb.public.list_author.name)
        FROM
            musicdb.public.songs
        JOIN
            musicdb.public.list_author ON musicdb.public.songs.from_author = musicdb.public.list_author.id
        WHERE
            musicdb.public.songs.songs_name LIKE '%' || text || '%';
    END IF;
END;
$$ LANGUAGE plpgsql;