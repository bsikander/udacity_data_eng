{#
  3NF - entity relationship diagram
  https://r766469c809452xjupyterlm1wubk29.udacity-student-workspaces.com/files/pagila-3nf.png

  star schema - entity relationship diagram
  https://r766469c809452xjupyterlm1wubk29.udacity-student-workspaces.com/files/pagila-star.png
#}

CREATE TABLE IF NOT EXISTS dimDate(
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

CREATE TABLE IF NOT EXISTS dimCustomer(
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

CREATE TABLE IF NOT EXISTS dimMovie(
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

CREATE TABLE IF NOT EXISTS dimStore(
    store_key int,
    store_id int,
    address text,
    address2 text,
    district text,
    city text,
    country text,
    postal_code text,
    manager_first_name text,
    manager_last_name text,
    start_date date,
    end_date date
);

INSERT INTO dimStore (store_key, store_id, address, address2, district, city, country, postal_code,
                         manager_first_name, manager_last_name, start_date, end_date)
SELECT  DISTINCT(s.store_id) AS store_key,
        s.store_id AS store_id,
        a.address AS address,
        a.address2 AS address2,
        a.district AS district,
        ci.city AS city,
        co.country AS country,
        a.postal_code AS postal_code,
        st.first_name AS manager_first_name,
        st.last_name AS manager_last_name,
        now()         AS start_date,
        now()         AS end_date
FROM store s
JOIN address a  ON (s.address_id = a.address_id)
JOIN city ci    ON (a.city_id = ci.city_id)
JOIN country co ON (ci.country_id = co.country_id)
JOIN staff st   ON (st.staff_id = s.manager_staff_id);

CREATE TABLE IF NOT EXISTS factSales(
    sales_key int,
    date_key int,
    customer_key int,
    movie_key int,
    store_key int,
    sales_amount float
);

INSERT INTO factSales (sales_key, date_key, customer_key, movie_key, store_key, sales_amount)
SELECT  DISTINCT(p.payment_id) AS sales_key,
        dimDate.date_key AS date_key,
        dimCustomer.customer_key AS customer_key,
        dimMovie.movie_key AS movie_key,
        dimStore.store_key AS store_key,
        p.amount AS sales_amount
FROM payment p
LEFT JOIN rental r     ON (r.rental_id = p.rental_id)
LEFT JOIN inventory i  ON (i.inventory_id = r.inventory_id)
LEFT JOIN dimStore     ON (i.store_id = dimStore.store_id)
LEFT JOIN dimCustomer  ON (r.customer_id = dimCustomer.customer_id)
LEFT JOIN dimMovie     ON (i.film_id = dimMovie.film_id)
LEFT JOIN dimDate      ON (p.payment_date = dimDate.date);
