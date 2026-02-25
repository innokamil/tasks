import json
from pathlib import Path
from typing import Dict, List
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString

def write_into_json(path: str | Path, obj: Dict | List[Dict]):
    with open(path, "w+") as f:
        json.dump(obj, f)

def write_into_xml(path: str | Path, obj: Dict | List[Dict]):
    xml = dicttoxml(obj)
    dom = parseString(xml)
    dom_prettified = dom.toprettyxml()
    with open(path, "w+") as f:
        f.write(dom_prettified)
