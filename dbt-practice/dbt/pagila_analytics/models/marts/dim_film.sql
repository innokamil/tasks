with rental_facts as (
    select * from {{ ref("int_rental_facts")}}
), film_actor_bridge as (
    select * from {{ ref("int_film_actor_bridge")}}
), film_rentals as (
    select 
        film_id,
        count(rental_id) as total_times_rented,
        sum(total_amount_paid) as total_revenue_generated
    from rental_facts 
    group by 1
)

select
    fac.film_id,
    fac.film_title,
    fac.description,
    fac.release_year,
    fac.rental_duration as standard_rental_duration_days,
    fac.rental_rate,
    fac.length as length_minutes,
    fac.replacement_cost,
    fac.rating,
    fac.category_id,
    fac.category_name,
    coalesce(fr.total_times_rented, 0) as total_times_rented,
    coalesce(fr.total_revenue_generated, 0.0) as total_revenue_generated
from film_actor_bridge fac 
join film_rentals fr using (film_id)
