import abc
import json
from pathlib import Path
from typing import Dict, List
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString

class ISerialize(abc.ABC):
    @abc.abstractmethod
    def _write_into_json(self, path: str | Path, obj: Dict | List[Dict]) -> bool:
        """
            Serialize an object into JSON file.

            Parameters:
                path: Save location.
                obj: Should be Dict-like or List of Dicts.

            Returns:
                True if saved.
        """
        try:
            with open(path, "w+") as f:
                json.dump(obj, f, default=str)
            return True
        except FileNotFoundError as e:
            print(f"Couldn't write into the file: {e}")
            return False

    @abc.abstractmethod
    def _write_into_xml(self, path: str | Path, obj: Dict | List[Dict]) -> bool:
        """
            Serialize an object into XML file.

            Parameters:
                path: Save location.
                obj: Should be Dict-like or List of Dicts.

            Returns:
                True if saved.
        """
        try:
            xml = dicttoxml(obj)
            dom = parseString(xml)
            with open(path, "w+") as f:
                f.write(dom.toprettyxml())
            return True
        except FileNotFoundError as e:
            print(f"Couldn't write into the file: {e}")
            return False

