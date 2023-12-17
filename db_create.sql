DROP EXTENSION IF EXISTS dblink;
CREATE EXTENSION IF NOT EXISTS dblink;

-- function to create database
DROP FUNCTION IF EXISTS create_db(text, text);
CREATE OR REPLACE FUNCTION create_db(dbname text)
RETURNS VOID AS
    $$
    BEGIN
        IF EXISTS (SELECT datname FROM pg_database WHERE datname = dbname) THEN
             RAISE NOTICE 'Database already exists';
        ELSE
             PERFORM dblink_exec('user=postgres password=1234 dbname= ' || current_database(),
                    'CREATE DATABASE ' || dbname);
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
                                    password varchar(30) NOT NULL
                                );

        CREATE TABLE IF NOT EXISTS list_author(
                                    id SERIAL PRIMARY KEY,
                                    name varchar(30) NOT NULL UNIQUE
                                );

        CREATE TABLE IF NOT EXISTS albums(
                                    albums_name varchar(30) PRIMARY KEY,
                                    year text NOT NULL UNIQUE,
                                    author_id integer NOT NULL,
                                    FOREIGN KEY (author_id) REFERENCES list_author (id) ON DELETE CASCADE
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
            songs_name varchar(40) NOT NULL UNIQUE,
            link text,
            txt_songs text,
            status integer default 0,
            from_album varchar(30) NOT NULL,
            FOREIGN KEY (from_album) REFERENCES albums (albums_name) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS favorite_songs(
                                    id SERIAL PRIMARY KEY,
                                    song_name varchar(40) NOT NULL,
                                    user_id integer NOT NULL,
                                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                                    FOREIGN KEY (song_name) REFERENCES songs (songs_name) ON DELETE CASCADE
        );
    END
    $$
LANGUAGE plpgsql;

--full drop db doesnt work now--
DROP FUNCTION IF EXISTS drop_database(text);
CREATE FUNCTION drop_database(dbname text)
	RETURNS VOID AS
	$$
	BEGIN
		IF EXISTS (SELECT datname FROM pg_database WHERE datname = dbname) THEN
			DROP DATABASE dbname;
		ELSE
			RAISE NOTICE 'Database does not exist';
		END IF;
	END
	$$
LANGUAGE plpgsql;

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

--insert into users albums--
DROP FUNCTION IF EXISTS insert_albums(VARCHAR(30),text, integer);
CREATE OR REPLACE FUNCTION insert_albums(albums_names VARCHAR(30), years text, author_ids integer)
    RETURNS VOID AS
    $$
    BEGIN
        INSERT INTO musicdb.public.albums (albums_name,year,author_id) VALUES (albums_names,years,author_ids);
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
DROP FUNCTION IF EXISTS insert_songs(varchar(40),text,text,integer,varchar(30));
CREATE OR REPLACE FUNCTION insert_songs(song_names varchar(40), links text, txt_songss text, statuss integer, from_albums varchar(30))
    RETURNS VOID AS
    $$
    BEGIN
        INSERT INTO musicdb.public.songs (songs_name,link,txt_songs,status,from_album) VALUES (song_names,links,txt_songss,statuss,from_albums);
    END;
    $$
LANGUAGE plpgsql;


--print for user tables--
DROP FUNCTION IF EXISTS select_users();
CREATE FUNCTION select_users()
    RETURNS TABLE(username VARCHAR, password VARCHAR) AS
    $$
    BEGIN
        RETURN QUERY
        SELECT musicdb.public.users.username, musicdb.public.users.password FROM musicdb.public.users;
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

--print for albums tables--
DROP FUNCTION IF EXISTS select_albums();
CREATE FUNCTION select_albums()
    RETURNS TABLE(albums_name VARCHAR, year text, author_id integer) AS
    $$
    BEGIN
        RETURN QUERY
        SELECT musicdb.public.albums.albums_name, musicdb.public.albums.year,musicdb.public.albums.author_id FROM musicdb.public.albums;
    END
	$$
LANGUAGE plpgsql;

--print for favorite_songs tables--
DROP FUNCTION IF EXISTS select_favorite_songs();
CREATE FUNCTION select_favorite_songs()
    RETURNS TABLE(song_name varchar(40), user_id integer) AS
    $$
    BEGIN
        RETURN QUERY
        SELECT musicdb.public.favorite_songs.song_name, musicdb.public.favorite_songs.user_id FROM musicdb.public.favorite_songs;
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
    RETURNS TABLE(id integer, songs_name varchar(40), link text, txt_songs text, status integer, from_album varchar(30)) AS
    $$
    BEGIN
        RETURN QUERY
        SELECT * FROM musicdb.public.songs;
    END
	$$
LANGUAGE plpgsql;

