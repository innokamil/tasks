with source as (
  select * from {{ source("pagila_raw", "PAGILA_CUSTOMER") }}
)

select
  cast(email as varchar(128)) as email,
  cast(store_id as smallint) as store_id,
  cast(address_id as smallint) as address_id,
  cast(first_name as varchar(32)) as first_name,
  cast(last_name as varchar(32)) as last_name,
  cast(customer_id as smallint) as customer_id,
  activebool as is_active,
  create_date,
  last_update
from source
