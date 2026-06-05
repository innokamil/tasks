with film_actor as (
  select * from {{ ref("stg_film_actor") }}
), film as (
  select * from {{ ref("stg_film") }}
), actor as (
  select * from {{ ref("stg_actor") }}
)

select
  f.title as film_title,
  fa.film_id,
  a.first_name || ' ' || a.last_name as actor_fullname,
  fa.actor_id,
  fa.last_update
from film_actor fa
join film f using (film_id)
join actor a using (actor_id)
