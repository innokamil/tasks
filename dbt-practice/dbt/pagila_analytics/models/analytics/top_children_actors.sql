with int_film_actor_bridge as (
    select * from {{ ref('int_film_actor_bridge') }}
),

dim_film as (
    select film_id, rating from {{ ref('dim_film') }}
)

select
    b.actor_id,
    b.actor_fullname,
    count(distinct b.film_id) as total_children_movies
from int_film_actor_bridge b
join dim_film f using (film_id)
where f.rating in ('G', 'PG')
group by 1, 2
order by total_children_movies desc
