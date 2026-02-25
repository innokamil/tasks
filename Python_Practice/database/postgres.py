from typing import Any, Dict 
from database.database import Database, DatabaseCredentials, QueryResult
import os
from pathlib import Path
import psycopg
from managers.resources import ResourceManager
from utils.readers import read_from_json
from datetime import datetime


class Postgres(Database):
    def __init__(self, 
                 credentials: DatabaseCredentials,
                 students_path: None | str,
                 rooms_path: None | str,
                 output: str):
        self.output: str = output
        self.dsn: str | None = credentials.into_dsn()
        assert self.dsn, f"'{self.dsn}' is not a valid DSN format."

        resource_dir: str | None = os.getenv("RESOURCES_DIRECTORY")
        assert resource_dir, f"""'{resource_dir}' is not a
        valid path for resource directory."""
        self.resource_manager: ResourceManager = ResourceManager(
            resource_dir,
            students=(students_path if students_path else "students.json"),
            rooms=(rooms_path if rooms_path else "rooms.json")
        )
        self.queries: Dict[str, str] = {
            "q1" : "select * from number_of_students_in_each_room",
            "q2" : "select * from top5_average_age_in_room",
            "q3" : "select * from top5_age_difference_in_room",
            "q4" : "select * from rooms_with_different_genders" 
        }
        self._initialize_schema()

    def select(self, stmt: str) -> QueryResult:
        with psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(stmt)
                res = QueryResult(
                    filename=("result"+str(int(datetime.timestamp(datetime.now())))),
                    colnames=[col[0] for col in cur.description],
                    records=cur.fetchall()
                )
                match self.output:
                    case "json":
                        res.write_into_json()
                    case "xml":
                        res.write_into_xml()
                return res

    def insert(self, stmt: str, items: Any):
        with psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.executemany(stmt, items)
            conn.commit()


    def _initialize_schema(self) -> None | bool:
        rooms_path: Path | None = self.resource_manager["rooms"]
        assert rooms_path, f"{rooms_path} is not a valid Path."

        rooms = read_from_json(rooms_path)
        assert rooms, f"Couldn't load json from {rooms_path}"

        students_path: Path | None = self.resource_manager["students"]
        assert students_path, f"{students_path} is not a valid Path."

        students = read_from_json(students_path)
        assert students,f"Couldn't load json from {students_path}"

        rooms_result = self.select(stmt="select * from rooms limit 1;")
        if len(rooms_result.records) <= 0:
            self.insert(
                stmt="insert into rooms(room_id, name) values (%s, %s)",
                items=((room["id"], room["name"]) for room in rooms))

        students_result = self.select(stmt="select * from students limit 1;")
        if len(students_result.records) <= 0:
            self.insert(
                stmt="insert into students(student_id, birthday, name, gender) values (%s, %s, %s, %s)",
                items=((student["id"], student["birthday"], 
                        student["name"], student["sex"]) for student in students),
            )

        room2student_result = self.select(stmt="select * from room2student limit 1;")
        if len(room2student_result.records) <= 0:
            self.insert(
                stmt="insert into room2student(room_id, student_id) values (%s, %s)",
                items= ((student["room"], student["id"]) for student in students)
            )
