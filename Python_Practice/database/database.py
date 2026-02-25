import abc
import os
from pathlib import Path
from typing import Any,  Tuple, List
from dataclasses import dataclass
from tabulate import tabulate
from utils.writers import write_into_json, write_into_xml

@dataclass
class QueryResult:
    filename: str
    colnames: List[str] 
    records: List[Tuple]
    """
    Representation of a Result after Querying in the Database class.

    Attributes:
        filename: Filename for query serialization.
        colnames: Column names present in the returned table.
        records: Data records in the table.
    """

    def __repr__(self) -> str:
        return tabulate(self.records, headers=self.colnames, tablefmt="grid")

    def write_into_json(self) -> bool:
        """
        Serialization into JSON file. Filename is deduced from the attribute `filename`.
        
        Returns:
            True if writing into JSON completed.
        """
        obj = list(map(lambda record: {
            k : v for k, v in zip(self.colnames, record)
        }, self.records))
        write_into_json(Path(os.getenv("RESOURCES_DIRECTORY"))/"dump"/self.filename,
                        obj)
        return True

    def write_into_xml(self) -> bool:
        """
        Serialization into XML file. Filename is deduced from the attribute `filename`.
        
        Returns:
            True if writing into XML completed.
        """
        obj = list(map(lambda record: {
            k : v for k, v in zip(self.colnames, record)
        }, self.records))
        write_into_xml(Path(os.getenv("RESOURCES_DIRECTORY"))/"dump"/self.filename,
                        obj)
        return True



@dataclass
class DatabaseCredentials:
    """
    Class for keeping a database connection information.
    """
    dbname: str
    port: str
    user: str
    password: str

    def __are_fields_valid(self) -> bool:
        """
        Check if fields are valid.

        Returns:
            True if fields are valid and can be used to construct a DSN string,
            otherwise False
        """
        return (
            len(self.dbname) != 0 and
            len(self.port) != 0 and
            len(self.user) != 0 and
            len(self.password) != 0
        )

    
    def into_dsn(self) -> str | None:
        """
        Construct a DSN from class fields.

        Returns:
            String in the DSN format if fields are valid, otherwise None that
            denotes a failure in constructing a DSN string.
        """
        return (
            f"dbname={self.dbname} "
                f"host=pgdb "
                f"port={self.port} "
                f"user={self.user} "
                f"password={self.password}"
        ) if self.__are_fields_valid() else None


class Database(abc.ABC):
    @abc.abstractmethod
    def _initialize_schema(self) -> None | bool:
        """
        Initializes the database schema, used for table initialization, etc.
        """
        ...

    @abc.abstractmethod
    def select(self, stmt: str) -> QueryResult:
        """
        Select data from the given statement.

        Parameters:
            stmt: Query statement, must `select` data.

        Returns:
            QueryResult class with data filled in.

        """
        ...

    @abc.abstractmethod
    def insert(self, stmt: str, items: Any):
        """
        Insert data into a table from the given statement.

        Parameters:
            stmt: Insert statement, must `insert` data.
            items: Items that will be inserted into the table declared in the `stmt` variable.
        """
        ...
