import abc
import json
from typing import Any 
from pathlib import Path

class IDeserialize(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def _read_from_json(cls, filename: str | Path) -> None | Any:
        """
        Read a JSON file contents.

        Parameters:
            filename: A full path to a file.

        Returns:
            Object of user choice, if reading failed then None is returned.
        """
        try:
            with open(filename, "r") as obj:
                return json.loads(obj.read()) 
        except FileNotFoundError as e:
            print(f"Couldn't open the file: {e}")
            return None


    @classmethod
    @abc.abstractmethod
    def _read_from_xml(cls, filename: str | Path) -> None | Any:
        """
        Read a XML file contents.

        Parameters:
            filename: A full path to a file.

        Returns:
            Object of user choice, if reading failed then None is returned.
        """
        try:
            with open(filename, "r") as obj:
                return obj.read()
        except FileNotFoundError as e:
            print(f"Couldn't open the file: {e}")
            return None
