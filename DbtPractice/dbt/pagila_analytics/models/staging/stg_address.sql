with source as (
  select * from {{ source("pagila_raw", "PAGILA_ADDRESS") }}
)

select 
  cast(phone as char(12)) as phone_number,
  cast(address_id as smallint) as address_id,
  cast(address as varchar(128)) as address,
  coalesce(cast(address2 as varchar(128)), 'unknown') as address2,
  cast(city_id as smallint) as city_id,
  cast(district as varchar(64)) as district,
  cast(postal_code as varchar(10)) as postal_code,
  last_update
from source
