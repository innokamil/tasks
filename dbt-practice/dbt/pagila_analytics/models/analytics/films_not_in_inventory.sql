with fact_rental as (
    select * from {{ ref("fact_rental") }}
), dim_film as (
    select * from {{ ref("dim_film") }}
)

select
    fr.film_id,
    f.film_title,
    f.release_year,
    f.rating
from fact_rental fr 
join dim_film f using (film_id)
where fr.inventory_id is null
