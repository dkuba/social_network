CREATE SCHEMA IF NOT EXISTS auth
    AUTHORIZATION postgres;

CREATE SCHEMA IF NOT EXISTS geo
    AUTHORIZATION postgres;

CREATE TYPE gender AS ENUM ('муж', 'жен');

CREATE TABLE IF NOT EXISTS auth.users
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

INSERT INTO geo.cities (id, name)
        SELECT gen_random_uuid (), 'Москва'
		WHERE NOT EXISTS
    (   SELECT  id
        FROM    geo.cities
        WHERE   name='Москва'
    );

