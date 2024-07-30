CREATE SCHEMA IF NOT EXISTS users
    AUTHORIZATION postgres;

CREATE SCHEMA IF NOT EXISTS geo
    AUTHORIZATION postgres;

CREATE TYPE gender AS ENUM ('муж', 'жен');

CREATE TABLE IF NOT EXISTS users.users
(
    id uuid NOT NULL,
    username character varying COLLATE pg_catalog."default" NOT NULL UNIQUE,
    password character varying COLLATE pg_catalog."default" NOT NULL,
    email character varying COLLATE pg_catalog."default" NOT NULL UNIQUE,
    first_name character varying COLLATE pg_catalog."default",
    last_name character varying COLLATE pg_catalog."default",
    date_of_birth date NOT NULL,
    user_gender gender NOT NULL,
    city uuid NOT NULL,
    interests text COLLATE pg_catalog."default",
    CONSTRAINT users_pkey PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS geo.cities
(
    id uuid NOT NULL,
    name character varying COLLATE pg_catalog."default" NOT NULL
);

CREATE TABLE IF NOT EXISTS users.user_friends
(
    user_one_id uuid NOT NULL,
    user_two_id uuid NOT NULL
);

CREATE TABLE IF NOT EXISTS users.posts
(
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    post_text TEXT NOT NULL,
    date_inserted TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO geo.cities (id, name)
        SELECT gen_random_uuid (), 'Москва'
		WHERE NOT EXISTS
    (   SELECT  id
        FROM    geo.cities
        WHERE   name='Москва'
    );


CREATE INDEX IF NOT EXISTS user_search_index ON users.users(username, first_name, last_name);
CREATE UNIQUE INDEX IF NOT EXISTS unique_user_friends_index ON users.user_friends(user_one_id, user_two_id);

