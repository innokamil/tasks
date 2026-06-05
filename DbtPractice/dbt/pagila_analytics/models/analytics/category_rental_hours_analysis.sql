with fact_rental as (
    select * from {{ ref('fact_rental') }}
),

dim_film as (
    select film_id, category_id from {{ ref('dim_film') }}
),

stg_category as (
    select * from {{ ref('stg_category') }}
)

select
    c.name as category_name,
    count(r.rental_id) as total_rentals,
    sum(datediff('hour', r.rental_date, r.return_date)) as total_rental_hours,
    round(avg(datediff('hour', r.rental_date, r.return_date)), 2) as avg_rental_hours
from fact_rental r
join dim_film f using(film_id)
join stg_category c using(category_id)
where r.return_date is not null
group by 1
order by total_rental_hours desc
