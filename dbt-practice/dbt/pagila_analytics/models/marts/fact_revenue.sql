with rental_facts as (
    select * from {{ ref('int_rental_facts') }}
)

select
    rf.rental_id,
    rf.customer_id,
    rf.film_id,
    rf.stored_id,
    rf.staff_id,
    cast(rf.rental_date as date) as revenue_date,
    rf.rental_date as revenue_timestamp,
    rf.total_amount_paid as gross_revenue,
    case 
        when rf.is_overdue = true then rf.total_amount_paid * 0.30  
        else 0 
    end as late_fee_revenue,
    case 
        when rf.is_overdue = false then rf.total_amount_paid
        else rf.total_amount_paid * 0.70                          
    end as base_rental_revenue,
    row_number() over (
        partition by rf.customer_id 
        order by rf.rental_date
    ) as customer_revenue_transaction_sequence,

    sum(rf.total_amount_paid) over (
        partition by rf.customer_id 
        order by rf.rental_date 
        rows between unbounded preceding and current row
    ) as customer_cumulative_clv_to_date

from rental_facts rf
