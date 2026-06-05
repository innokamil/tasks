with source as (
  select * from {{ source("pagila_raw", "PAGILA_INVENTORY") }}
)

select
  cast(film_id as smallint) as film_id,
  cast(store_id as tinyint) as stored_id,
  cast(inventory_id as smallint) as inventory_id,
  last_update
from
  source


