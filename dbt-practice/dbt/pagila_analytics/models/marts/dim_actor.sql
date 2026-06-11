with actor_bridge as (
    select * from {{ ref('int_film_actor_bridge') }}
),

actor_counts as (
    select 
        actor_id,
        count(distinct film_id) as total_films_starred
    from actor_bridge
    group by 1
)

select
    ab.actor_id,
    ab.first_name,
    ab.last_name,
    ab.actor_fullname,
    coalesce(ac.total_films_starred, 0) as total_films_starred
from actor_bridge ab
left join actor_counts ac using (actor_id)
