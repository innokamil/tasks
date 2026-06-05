with fact_rental as (
    select * from {{ ref('fact_rental') }}
),

dim_film as (
    select film_id, category_name from {{ ref('dim_film') }}
),

stg_category as (
    select * from {{ ref('stg_category') }}
)

select
    f.category_name,
    sum(r.total_amount_paid) as total_revenue,
    count(r.rental_id) as total_rentals
from fact_rental r
join dim_film f using (film_id) 
group by 1
order by total_revenue desc
