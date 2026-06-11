with fact_rental as (
    select * from {{ ref('fact_rental') }}
),

dim_film as (
    select film_id, category_id, category_name from {{ ref('dim_film') }}
)

select
    f.category_id,
    f.category_name as category_name,
    count(fr.rental_id) as total_rentals,
    sum(datediff('hour', fr.rental_date, fr.return_date)) as total_rental_hours,
    round(avg(datediff('hour', fr.rental_date, fr.return_date)), 2) as avg_rental_hours
from fact_rental fr
join dim_film f using(film_id)
where fr.return_date is not null
group by 1, 2
order by total_rental_hours desc
