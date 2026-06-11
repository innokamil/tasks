with rental_facts as (
    select * from {{ ref('int_rental_facts') }}
)

select
    rf.rental_id,
    rf.customer_id,
    rf.film_id,
    rf.stored_id,
    rf.staff_id,
    rf.inventory_id,
    rf.rental_date,
    rf.return_date,
    cast(rf.rental_date as date) as rental_date_day,
    rf.actual_duration_days,
    rf.allowed_duration_days,
    case 
        when rf.actual_duration_days > rf.allowed_duration_days 
            then (rf.actual_duration_days - rf.allowed_duration_days)
        else 0
    end as days_overdue,
    1 as rental_volume, 
    case when rf.is_overdue = true then 1 else 0 end as is_overdue_volume,
    case when rf.return_date is null then 1 else 0 end as is_currently_outstanding_volume,
    row_number() over (
        partition by rf.customer_id 
        order by rf.rental_date
    ) as customer_rental_lifetime_sequence
from rental_facts rf
