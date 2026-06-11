with fact_revenue as (
    select * from {{ ref('fact_revenue') }}
),

int_film_actor_bridge as (
    select * from {{ ref('int_film_actor_bridge') }}
)

select
    b.actor_id,
    b.actor_fullname,
    count(r.rental_id) as total_rentals_generated,
    sum(r.gross_revenue) as total_revenue_generated
from fact_revenue r
join int_film_actor_bridge b using (film_id)
group by 1, 2
order by total_rentals_generated desc
