import abc
from pathlib import Path
from typing import Any, Dict,  Tuple, List
from dataclasses import dataclass
from tabulate import tabulate
from utils.readers import IDeserialize
from utils.writers import ISerialize

@dataclass
class QueryResult(ISerialize, IDeserialize):
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
    def _write_into_json(self, path: str | Path, obj: Dict | List[Dict])->bool:
        return super()._write_into_json(path, obj)

    def _write_into_xml(self, path: str | Path, obj: Dict | List[Dict])->bool:
        return super()._write_into_xml(path, obj)
    
    @classmethod
    def _read_from_json(cls, filename: str | Path) -> None | Any:
        # Now return just string / object but deserialize it into this class and
        # return it
        return super()._read_from_json(filename)
    @classmethod
    def _read_from_xml(cls, filename: str | Path) -> None | Any:
        return super()._read_from_xml(filename)

    def __repr__(self) -> str:
        return tabulate(self.records, headers=self.colnames, tablefmt="grid")


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
