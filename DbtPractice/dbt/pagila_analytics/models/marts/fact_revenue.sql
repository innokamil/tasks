with stg_payment as (
    select * from {{ ref('stg_payment') }}
)

select
    payment_id,
    customer_id,
    rental_id,
    amount as revenue_amount,
    payment_date as revenue_timestamp,
    cast(payment_date as date) as revenue_date
from stg_payment
