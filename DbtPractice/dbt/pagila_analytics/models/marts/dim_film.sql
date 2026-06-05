with stg_film as (
    select * from {{ ref('stg_film') }}
),

stg_category as (
    select * from {{ ref('stg_category') }}
),

stg_film_category as (
    select * from {{ ref("stg_film_category") }}
),

film_rentals as (
    select 
        film_id,
        count(rental_id) as total_times_rented,
        sum(total_amount_paid) as total_revenue_generated
    from {{ ref('int_rental_facts') }}
    group by 1
)

select
    f.film_id,
    f.title as film_title,
    f.description,
    f.release_year,
    f.rental_duration as standard_rental_duration_days,
    f.rental_rate,
    f.length as length_minutes,
    f.replacement_cost,
    f.rating,
    c.category_id,
    c.name as category_name,
    coalesce(fr.total_times_rented, 0) as total_times_rented,
    coalesce(fr.total_revenue_generated, 0.0) as total_revenue_generated
from stg_film f
left join film_rentals fr using(film_id)
left join stg_film_category fc using (film_id)
join stg_category c using (category_id)
