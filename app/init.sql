CREATE SCHEMA IF NOT EXISTS auth
    AUTHORIZATION postgres;

CREATE SCHEMA IF NOT EXISTS auth
    AUTHORIZATION postgres;

CREATE TABLE IF NOT EXISTS auth.users
(
    id uuid NOT NULL,
    username character varying COLLATE pg_catalog."default" NOT NULL,
    password character varying COLLATE pg_catalog."default" NOT NULL,
    email character varying COLLATE pg_catalog."default" NOT NULL,
    first_name character varying COLLATE pg_catalog."default",
    last_name character varying COLLATE pg_catalog."default",
    date_of_birth date NOT NULL,
    city uuid NOT NULL,
    interests text COLLATE pg_catalog."default",
    CONSTRAINT users_pkey PRIMARY KEY (id)
)

ALTER TABLE IF EXISTS auth.users
    OWNER to postgres;

CREATE TABLE IF NOT EXISTS geo.cities
(
    id uuid NOT NULL,
    name character varying COLLATE pg_catalog."default" NOT NULL
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS geo.cities
    OWNER to postgres;
