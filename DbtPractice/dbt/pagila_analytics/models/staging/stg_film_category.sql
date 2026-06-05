with source as (
  select * from {{ source("pagila_raw", "PAGILA_FILM_CATEGORY")}}
)

select
  cast(film_id as smallint) as film_id,
  cast(category_id as smallint) as category_id,
  last_update
from source
