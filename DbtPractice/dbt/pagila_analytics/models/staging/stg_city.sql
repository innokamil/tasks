with source as (
  select * from {{ source("pagila_raw", "PAGILA_CITY") }}
)

select
  cast(city_id as smallint) as city_id,
  cast(city as varchar(64)) as name,
  cast(country_id as smallint) as country_id,
  last_update
from source

