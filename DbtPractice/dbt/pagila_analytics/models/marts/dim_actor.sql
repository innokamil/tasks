with actor_bridge as (
    select * from {{ ref('int_film_actor_bridge') }}
),

stg_actor as (
    select 
        actor_id,
        first_name,
        last_name,
        first_name || ' ' || last_name as actor_full_name
    from {{ ref('stg_actor') }}
),

actor_counts as (
    select 
        actor_id,
        count(distinct film_id) as total_films_starred
    from actor_bridge
    group by 1
)

select
    a.actor_id,
    a.first_name,
    a.last_name,
    a.actor_full_name,
    coalesce(ac.total_films_starred, 0) as total_films_starred
from stg_actor a
left join actor_counts ac using (actor_id)
