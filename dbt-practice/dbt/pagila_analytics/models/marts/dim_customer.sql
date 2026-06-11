with customer_enriched as (
    select * from {{ ref('int_customer_enriched') }}
),

rental_facts as (
    select 
        customer_id,
        count(rental_id) as total_rentals,
        sum(total_amount_paid) as total_spent
    from {{ ref('int_rental_facts') }}
    group by 1
)

select
    c.customer_id,
    c.customer_fullname,
    c.email,
    c.is_active,
    c.address,
    c.district,
    c.postal_code,
    c.phone_number,
    c.name as city_name,
    coalesce(r.total_rentals, 0) as total_rentals_lifetime,
    coalesce(r.total_spent, 0.0) as total_spent_lifetime,
    c.create_date as customer_since_date
from customer_enriched c
left join rental_facts r using (customer_id)
