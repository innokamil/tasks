from database.database import DatabaseCredentials
from database.postgres import Postgres
import argparse

def main():
    parser = argparse.ArgumentParser(description="Python BigData Task 1.")
    parser.add_argument("-s", "--students", required=False, 
                        default=None, help="Path to the students.json")
    parser.add_argument("-r", "--rooms", required=False, 
                        default=None, help="Path to the rooms.json")
    parser.add_argument("-o", "--output", required=False, choices=['json', 'xml'],
                        default="json", help="Format of the query result")
    parser.add_argument("-q", "--query", required=False, default="q1", 
                        choices=["q1", "q2", "q3", "q4"], 
                        help="Answer to the question")
    args = parser.parse_args()
    dc = DatabaseCredentials(dbname="task1", 
                             port="5432", 
                             user="innowise",
                             password="innowise")
    pgdb = Postgres(credentials=dc, students_path=args.students,
                    rooms_path=args.rooms, output=args.output)
    res = pgdb.select(stmt=pgdb.queries[args.query])
    print(f"Saved in: {res.filename}")



if __name__=="__main__":
    main()
