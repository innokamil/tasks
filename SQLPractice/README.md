# Introduction
Task based on the following [repo](https://github.com/devrimgunduz/pagila).

___
# 1. Output the number of movies in each category, sorted descending.
```postgres 
select c.name, count(*) as cnt
from film_category fc
join category c using (category_id)
group by c.name
order by cnt desc;
```
___
# 2. Output the 10 actors whose movies rented the most, sorted in descending order.
```postgres
with films_rented as (
	select i.film_id, count(*) as cnt
	from inventory i
	join rental r using (inventory_id)
	group by i.film_id 
	order by cnt desc
), actors_in_films as (
	select film_id, first_name || ' ' || last_name as actor 
	from film_actor fa 
	join actor a using (actor_id)
)

select * from actors_in_films
join films_rented rs using (film_id)
order by cnt desc
limit 10;
```
___
# 3. Output the category of movies on which the most money was spent.
```postgres
with films_rented_with_amount as (
	select i.film_id, p.amount
	from inventory i
	join rental r using (inventory_id)
	join payment p using (rental_id)
), films_and_categories as (
	select film_id, title, name as category_name
	from film
	join film_category fc using (film_id)
	join category c using (category_id)
)

select category_name, sum(amount) from films_and_categories
join films_rented_with_amount using (film_id)
group by category_name 
order by sum(amount) desc;
```
___
# 4. Print the names of movies that are not in the inventory. Write a query without using the `IN` operator.
```postgres
-- join
select f.title
from film f
left join inventory i using (film_id)
where i.film_id is null;

-- exists
select f.title
from film f
where not exists (
	select i.film_id
	from inventory i
	where f.film_id = i.film_id);

-- IN
select title
from film
where 
film_id in (
	select film_id
	from film
except
	select film_id
	from inventory);
```
___
# 5. Output the top 3 actors who have appeared the most in movies in the “Children” category. If several actors have the same number of movies, output all of them.
```postgres
with films_and_actors as (
	select f.film_id, fa.actor_id, f.title
	from film_actor fa
	join film f using (film_id)
), films_and_categories as (
	select c.category_id, fc.film_id, c.name as category_name
	from film_category fc
	join category c using (category_id)
), actor_rankings as(
	select 
		a.first_name || ' ' || a.last_name as fullname, 
		count(faa.title) as movie_count,
		dense_rank() over (order by count(faa.title) desc) ranked
	from actor a
	join films_and_actors faa using (actor_id)
	join films_and_categories fac using (film_id)
	where fac.category_name = 'Children'
	group by a.actor_id, fullname
	order by movie_count desc
)

select fullname, movie_count
from actor_rankings
where ranked <= 3;
```
___
# 6. Output cities with the number of active and inactive customers (active - customer.active = 1). Sort by the number of inactive customers in descending order.
```postgres
with customers_with_addresses as (
	select a.city_id, cu.customer_id, cu.first_name, cu.last_name, cu.active
	from customer cu
	join address a using (address_id)
)

select 
	c.city, 
	count(*) as customers, 
	count(*) filter (where acwa.active=1) as active_customers,
	count(*) filter (where acwa.active=0) as inactive_customers
from customers_with_addresses acwa
join city c using (city_id)
group by c.city
```
___
# 7. Output the category of movies that have the highest number of total rental hours in the city (customer.address_id in this city) and that start with the letter “a”. Do the same for cities that have a “-” in them. Write everything in one query.
```postgres
with rental_stats as (
select
	case
		when ci.city ilike 'a%' then 'A*'
		when ci.city ilike '%-%' then '*-*'
	end as city_group,
	cat.name as category_name,
	sum(extract(epoch from (r.return_date - r.rental_date)) / 3600) as total_hours
from city ci
join address a using (city_id)
join customer c using(address_id)
join rental r using (customer_id)
join inventory i using (inventory_id)
join film_category fc using (film_id)
join category cat using (category_id)
where ci.city ilike 'a%' or ci.city like '%-%'
group by 1, 2)

select
	distinct on
	(city_group)
    city_group,
	category_name,
	ROUND(total_hours::numeric, 2) as total_hours
from rental_stats
order by city_group, total_hours desc;
```