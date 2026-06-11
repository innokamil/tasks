with date_spine as (
    select 
        dateadd(day, seq4(), '2020-01-01'::date) as date_day
    from table(generator(rowcount => 3650))
)

select
    date_day as date_id,
    date_day as date_actual,
    extract(year from date_day) as year,
    extract(month from date_day) as month_number,
    to_char(date_day, 'MMMM') as month_name,
    extract(day from date_day) as day_of_month,
    extract(quarter from date_day) as quarter,
    extract(dayofweek from date_day) as day_of_week_number,
    to_char(date_day, 'DY') as day_of_week_name
from date_spine
