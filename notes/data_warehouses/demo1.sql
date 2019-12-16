{#
  3NF - entity relationship diagram
  https://r766469c809452xjupyterlm1wubk29.udacity-student-workspaces.com/files/pagila-3nf.png

  star schema - entity relationship diagram
  https://r766469c809452xjupyterlm1wubk29.udacity-student-workspaces.com/files/pagila-star.png
#}

CREATE TABLE dimDate(
    date_key int,
    date date,
    year smallint,
    quarter smallint,
    month smallint,
    day smallint,
    week smallint,
    is_weekend bool
);

INSERT INTO dimDate (date_key, date, year, quarter, month, day, week, is_weekend)
SELECT DISTINCT(TO_CHAR(payment_date :: DATE, 'yyyyMMDD')::integer) AS date_key,
       date(payment_date)                                           AS date,
       EXTRACT(year FROM payment_date)                              AS year,
       EXTRACT(quarter FROM payment_date)                           AS quarter,
       EXTRACT(month FROM payment_date)                             AS month,
       EXTRACT(day FROM payment_date)                               AS day,
       EXTRACT(week FROM payment_date)                              AS week,
       CASE WHEN EXTRACT(ISODOW FROM payment_date) IN (6, 7) THEN true ELSE false END AS is_weekend
FROM payment;

CREATE TABLE dimCustomer(
    customer_key int,
    customer_id int,
    first_name text,
    last_name text,
    email text,
    address text,
    address2 text,
    district text,
    city text,
    country text,
    postal_code text,
    phone text,
    active text,
    create_date date,
    start_date date,
    end_date date
);

INSERT INTO dimCustomer (customer_key, customer_id, first_name, last_name, email, address,
                         address2, district, city, country, postal_code, phone, active,
                         create_date, start_date, end_date)
SELECT  DISTINCT(c.customer_id) AS customer_key,
        c.customer_id AS customer_id,
        c.first_name AS first_name,
        c.last_name AS last_name,
        c.email AS email,
        a.address AS address,
        a.address2 AS address2,
        a.district AS district,
        ci.city AS city,
        co.country AS country,
        a.postal_code AS postal_code,
        a.phone AS phone,
        c.active AS active,
        c.create_date AS create_date,
        now()         AS start_date,
        now()         AS end_date
FROM customer c
JOIN address a  ON (c.address_id = a.address_id)
JOIN city ci    ON (a.city_id = ci.city_id)
JOIN country co ON (ci.country_id = co.country_id);

CREATE TABLE dimMovie(
    movie_key int,
    film_id int,
    title text,
    description text,
    release_year int,
    language text,
    original_language text,
    rental_duration int,
    length int,
    rating text,
    special_features text
);

INSERT INTO dimMovie (movie_key, film_id, title, description, release_year, language, original_language, rental_duration, length, rating, special_features)
SELECT  DISTINCT(f.film_id) AS movie_key,
        f.film_id AS film_id,
        f.title AS title,
        f.description AS description,
        f.release_year AS release_year,
        l.name AS language,
        orig_lang.name AS original_language,
        f.rental_duration AS rental_duration,
        f.length AS length,
        f.rating AS rating,
        f.special_features AS special_features
FROM film f
JOIN language l              ON (f.language_id=l.language_id)
LEFT JOIN language orig_lang ON (f.original_language_id = orig_lang.language_id);
