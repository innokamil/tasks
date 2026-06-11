with film_actor as (
  select * from {{ ref("stg_film_actor") }}
), film as (
  select * from {{ ref("stg_film") }}
), actor as (
  select * from {{ ref("stg_actor") }}
), film_category as (
  select * from {{ ref("stg_film_category") }}
), category as (
  select * from {{ ref("stg_category") }}
)

select
  f.title as film_title,
  f.length,
  f.rating,
  f.film_id,
  f.fulltext,
  f.description,
  f.language_id,
  f.original_language_id,
  f.release_year,
  f.rental_duration,
  f.rental_rate,
  f.replacement_cost,
  f.special_features,
  c.category_id,
  c.name as category_name,
  a.actor_id,
  a.first_name,
  a.last_name,
  a.first_name || ' ' || a.last_name as actor_fullname
from film_actor fa
join film f using (film_id)
join film_category fc using (film_id)
join category c using (category_id)
join actor a using (actor_id)
