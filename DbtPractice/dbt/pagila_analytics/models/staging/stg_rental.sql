with source as (
  select * from {{ source("pagila_raw", "PAGILA_RENTAL") }}
)

select
  cast(staff_id as smallint) as staff_id,
  cast(rental_id as smallint) as rental_id ,
  cast(inventory_id as smallint) as inventory_id,
  cast(customer_id as smallint) as customer_id,
  rental_date,
  return_date,
  last_update,
from source
