with rental as (
    select * from {{ ref('stg_rental') }}
),

inventory as (
    select * from {{ ref('stg_inventory') }}
),

film as (
    select film_id, title, rental_duration from {{ ref('stg_film') }}
),

payment as (
    select rental_id, sum(amount) as total_amount_paid
    from {{ ref('stg_payment') }}
    group by 1
)

select
    r.rental_id,
    r.customer_id,
    r.rental_date,
    r.return_date,
    i.film_id,
    f.title as film_title,
    coalesce(p.total_amount_paid, 0) as total_amount_paid,
    datediff('day', r.rental_date, r.return_date) as actual_duration_days,
    f.rental_duration as allowed_duration_days,
    case 
        when datediff('day', r.rental_date, r.return_date) > f.rental_duration then true
        else false
    end as is_overdue
from rental r
join inventory i using (inventory_id)
join film f using (film_id)
left join payment p using (rental_id)
