with stg_film as (
    select * from {{ ref('stg_film') }}
),

stg_inventory as (
    select * from {{ ref('stg_inventory') }}
)

select
    f.film_id,
    f.title as film_title,
    f.release_year,
    f.rating
from stg_film f
left join stg_inventory i using (film_id) 
where i.inventory_id is null
