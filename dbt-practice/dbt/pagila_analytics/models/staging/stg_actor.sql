with source as (
  select * from {{ source("pagila_raw", "PAGILA_ACTOR") }}
)

select 
  cast(actor_id as number) as actor_id,
  cast(first_name as varchar(64)) as first_name,
  cast(last_name as varchar(64)) as last_name,
  last_update
from source
