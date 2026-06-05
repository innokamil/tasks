with source as (
  select * from {{ source("pagila_raw", "PAGILA_FILM") }}
)

select
  cast(title as varchar(64)) as title,
  cast(length as smallint) as length,
  cast(rating as varchar(6)) as rating,
  cast(film_id as smallint) as film_id,
  cast(fulltext as varchar(1024)) as fulltext,
  cast(description as varchar(1024)) as description,
  cast(language_id as smallint) as language_id,
  cast(original_language_id as smallint) as original_language_id, 
  cast(release_year as smallint) as release_year,
  cast(rental_duration as tinyint) as rental_duration,
  rental_rate,
  replacement_cost,
  special_features,
  last_update
from source
