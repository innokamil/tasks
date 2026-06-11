with dim_film as (
    select film_id, category_name from {{ ref('dim_film') }}
), fact_revenue as (
    select * from {{ ref("fact_revenue") }}
)

select
    f.category_name,
    sum(fr.gross_revenue) as total_revenue,
    count(fr.rental_id) as total_rentals
from fact_revenue as fr
join dim_film f using (film_id) 
group by 1
order by total_revenue desc
