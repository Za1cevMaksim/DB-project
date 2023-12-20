-- create trigger that add social media after list_author
DROP FUNCTION IF EXISTS add_default_socialmedia();
CREATE OR REPLACE FUNCTION add_default_socialmedia()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO musicdb.public.socialmedia(author_id, instagram,twitter,any_other) VALUES (NEW.id, 'NONE', 'NONE','NONE');
    RETURN NULL;
END
$$ LANGUAGE plpgsql;


CREATE TRIGGER add_default_socialmedia_trigger
AFTER INSERT
ON musicdb.public.list_author
FOR EACH ROW
EXECUTE FUNCTION add_default_socialmedia();