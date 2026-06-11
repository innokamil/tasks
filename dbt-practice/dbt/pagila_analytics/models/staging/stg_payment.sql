with source as (
  select * from {{ source("pagila_raw", "PAGILA_PAYMENT") }}
)

select
  amount,
  cast(staff_id as smallint) as staff_id,
  cast(rental_id as smallint) as rental_id,
  cast(payment_id as smallint) as payment_id,
  cast(customer_id as smallint) as customer_id,
  payment_date
from source

