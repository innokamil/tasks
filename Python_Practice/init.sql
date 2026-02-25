create table if not exists rooms(
  room_id bigserial,
  name varchar(32),
  primary key (room_id)
);

create table if not exists students(
  student_id bigserial,
  birthday timestamptz,
  name text not null,
  gender char(1),
  primary key (student_id)
);

create table if not exists room2student(
  ID bigserial,
  room_id bigint not null references rooms(room_id),
  student_id bigint not null references students(student_id),
  primary key (ID)
);

-- Q1. Solution
create view number_of_students_in_each_room as (
select rs.room_id as Room, count(*) as Students
from room2student rs
group by rs.room_id
);

-- Q2. Solution
create view top5_average_age_in_room as (
select
  rs.room_id,
  avg(extract(year from AGE(s.birthday))) as avg_age
from students s
join room2student rs using (student_id)
group by rs.room_id
order by avg_age asc
limit 5
);

-- Q3. Solution
create view students_in_room as (
select 
  rs1.room_id,
  rs1.student_id as first_student,
  rs2.student_id as second_student
from room2student rs1 join room2student rs2 using (room_id)
where rs1.student_id < rs2.student_id
);

create view top5_age_difference_in_room as (
select 
  sir.room_id,
  max(abs(extract(year from AGE(s1.birthday)) - extract(year from AGE(s2.birthday)))) as age_diff
from students_in_room sir join students s1 on s1.student_id = first_student
join students s2 on s2.student_id = second_student
group by sir.room_id
order by age_diff desc
limit 5
);

-- Q4. Solution
create view rooms_with_different_genders as (
select
  distinct sir.room_id
from students_in_room sir
join students s1 on s1.student_id = first_student
join students s2 on s2.student_id = second_student
where s1.gender != s2.gender
);

-- Indexes
create index index_student_birthday on students(birthday);
create index index_room_to_student_student_id on room2student(student_id);
create index index_room_to_student_room_id on room2student(room_id);

