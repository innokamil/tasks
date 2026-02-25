import json
from typing import Any 
from pathlib import Path

def read_from_json(filename: str | Path) -> None | Any:
    """
    Read a JSON file contents.

    Parameters:
        filename: A full path to a file.

    Returns:
        JSON object if read successfully otherwise None.
    """
    with open(filename, "r") as obj:
        return json.loads(obj.read()) 

def read_from_xml(filename: str | Path) -> None | Any:
    """
    Read a XML file contents.

    Parameters:
        filename: A full path to a file.

    Returns:
        XML object if read successfully otherwise None.
    """

    with open(filename, "r") as obj:
        return obj.read()
