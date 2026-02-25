# Problem statement
Using MySQL database (or other relational database, for example, PostgreSQL) to create a data schema corresponding to the files in the attachment (many-to-one relationship). Write a script to load these two files and write data to the database.
___
## Necessary queries to the database
-   List of rooms and the number of students in each of them
-   5 rooms with the smallest average age of students
-   5 rooms with the largest difference in the age of students
-   List of rooms where different-sex students live
___
## Requirements and comments
1.  Propose options for optimizing queries using indexes
2.  As a result we need to generate a SQL query that adds the required indexes.
3.  Unload the result in JSON or XML format
4.  All the “math” should be done at the database level
5.  The command interface should support the following input parameters
    5.1. students (path to students file)
    5.2. rooms (path to the rooms file)
    5.3. format (output format: xml or json)
    5.4. use OOP and SOLID
    5.5. no ORM (use SQL)
___
## Before you begin the task:
-   Make sure you have understood the condition correctly 
-   Created and configured the virtual environment 
-   Designed the architecture 
-   Decomposed into subtasks in Jira ticket
