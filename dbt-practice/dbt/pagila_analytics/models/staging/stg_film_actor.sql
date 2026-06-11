with source as (
  select * from {{ source("pagila_raw", "PAGILA_FILM_ACTOR") }}
)
select
    cast(actor_id as smallint) as actor_id,
    cast(film_id as smallint) as film_id,
    last_update 
from source 
