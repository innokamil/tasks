with fact_rental as (
    select * from {{ ref("fact_rental") }}
), dim_film as (
    select * from {{ ref('dim_film') }}
)

select
    f.category_id,
    f.category_name,
    count(fr.film_id) as total_titles,
    round(avg(f.rental_rate), 2) as avg_rental_rate,
    round(avg(f.replacement_cost), 2) as avg_replacement_cost
from fact_rental fr
join dim_film f using (film_id)
group by 1, 2
order by total_titles desc
