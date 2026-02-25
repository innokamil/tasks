import abc
import json
from pathlib import Path
from typing import Dict, List
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString

class ISerialize(abc.ABC):
    @abc.abstractmethod
    def _write_into_json(self, path: str | Path, obj: Dict | List[Dict]) -> bool:
        with open(path, "w+") as f:
            json.dump(obj, f)
        return True

    @abc.abstractmethod
    def _write_into_xml(self, path: str | Path, obj: Dict | List[Dict]) -> bool:
        xml = dicttoxml(obj)
        dom = parseString(xml)
        dom_prettified = dom.toprettyxml()
        with open(path, "w+") as f:
            f.write(dom_prettified)
        return True
