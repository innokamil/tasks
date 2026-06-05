with customer as (
    select * from {{ ref('stg_customer') }}
),

address as (
    select * from {{ ref('stg_address') }}
),

city as (
    select * from {{ ref('stg_city') }}
)

select
    c.customer_id,
    c.first_name,
    c.last_name,
    c.first_name || ' ' || c.last_name as customer_fullname,
    c.email,
    c.is_active,
    a.address,
    a.district,
    a.postal_code,
    a.phone_number,
    ci.name,
    c.create_date,
    c.last_update
from customer c
join address a using (address_id)
join city ci using (city_id)
