with rental_facts as (
    select * from {{ ref('int_rental_facts') }}
)

select
    rental_id,
    customer_id,
    film_id,
    rental_date,
    return_date,
    actual_duration_days,
    allowed_duration_days,
    is_overdue,
    total_amount_paid
from rental_facts
