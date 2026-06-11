with dim_customer as (
    select * from {{ ref('dim_customer') }}
)

select
    city_name,
    count(customer_id) as total_customers,
    sum(total_rentals_lifetime) as total_rentals,
    sum(total_spent_lifetime) as total_revenue
from dim_customer
group by 1
order by total_customers desc
