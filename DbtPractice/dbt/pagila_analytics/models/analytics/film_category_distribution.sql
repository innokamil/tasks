with dim_film as (
    select * from {{ ref('dim_film') }}
),

stg_category as (
    select * from {{ ref('stg_category') }}
)

select
    c.name as category_name,
    count(f.film_id) as total_titles,
    round(avg(f.rental_rate), 2) as avg_rental_rate,
    round(avg(f.replacement_cost), 2) as avg_replacement_cost
from dim_film f
join stg_category c using (category_id)
group by 1
order by total_titles desc
