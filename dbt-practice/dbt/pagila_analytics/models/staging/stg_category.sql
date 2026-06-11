with source as (
  select * from {{ source("pagila_raw", "PAGILA_CATEGORY") }}
)

select
  cast(category_id as tinyint) as category_id,
  cast(name as varchar(16)) as name,
  last_update
from source
