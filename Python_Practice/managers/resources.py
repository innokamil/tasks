import os
from pathlib import Path
from typing import Dict, List, Any
from database.database import QueryResult
from utils.readers import IDeserialize
from utils.writers import ISerialize


class ResourceManager(IDeserialize, ISerialize):
    def __init__(self, root_directory: str, dump_dir: str, **kwargs):
        """
        Managing resources, pass directories by its name (they will be prepended
        by `root_directory`). Example: 
            resource_manager: ResourceManager = ResourceManager("root", "dump", ...)

        Attributes:
            root_directory: A root directory, that will be used for path managing.
            dump_dir: A directory where results are saved.
            resource_paths: Stores paths, all start with `root_directory`.
        """
        self.root_directory: Path = Path(root_directory)
        self.dump_dir: Path = self.construct_path(dump_dir)
        self.resource_paths: Dict[str, Path] = {
            k : self.construct_path(v) for k, v in kwargs.items()
        } 

    def read_result(self, what: str) -> Any:
        location: Path = self.dump_dir / what
        ext: None | str = None
        if what[-4::] == "json":
            ext = "json"
        elif what[-3::] == "xml":
            ext = "xml"
        if not ext:
            raise ValueError(f"Couldn't determine the extension of the file {ext}")
        match ext:
            case "json":
                return self._read_from_json(location)
            case "xml":
                return self._read_from_xml(location)

    def write_into_json(self, path: str, obj: Dict | List[Dict]) -> bool:
        pathname = self[path]
        if not pathname:
            print(f"{path} not in the resource paths.")
            return False 
        return self._write_into_json(path, obj)

    def _write_into_json(self, path: str | Path, obj: Dict | List[Dict]) -> bool:
        return super()._write_into_json(path, obj)

    def write_into_xml(self, path: str, obj: Dict | List[Dict]) -> bool:
        pathname = self[path]
        if not pathname:
            print(f"{path} not in the resource paths.")
            return False 
        return self._write_into_xml(path, obj)

    def _write_into_xml(self, path: str | Path, obj: Dict | List[Dict]) -> bool:
        return super()._write_into_xml(path, obj)
    
    def read_from_json(self, filename: str) -> None | Any:
        pathname = self[filename]
        if not pathname:
            print(f"{pathname} not in the resource paths.")
            return None 
        return self._read_from_json(pathname)

    @classmethod
    def _read_from_json(cls, filename: str | Path) -> None | Any:
        return super()._read_from_json(filename)

    def read_from_xml(self, filename: str) -> None | Any:
        pathname = self[filename]
        if not pathname:
            print(f"{pathname} not in the resource paths.")
            return None
        return self._read_from_xml(pathname)

    @classmethod
    def _read_from_xml(cls, filename: str | Path) -> None | Any:
        return super()._read_from_xml(filename)

    def serialize_query(self, obj: QueryResult, output: str = "json"):
        location: Path = self.dump_dir / obj.filename
        obj_dictlike: List[Dict] = list(map(lambda record: {
            k : v for k, v in zip(obj.colnames, record)
        }, obj.records))
        match output:
            case "json":
                obj._write_into_json(location, obj_dictlike)
            case "xml":
                obj._write_into_xml(location, obj_dictlike)

    def deserialize_query(self, filename: str | Path, output: str = "json") -> Any | None:
        location: Path = self.dump_dir / filename
        match output:
            case "json":
                return QueryResult._read_from_json(location)
            case "xml":
                return QueryResult._read_from_xml(location)

    def __getitem__(self, key: str) -> Path | None:
        """
        Get a filepath from `resource_paths` by a key.

        Parameters:
            key: A path name.

        Returns:
            Path if a resource path exists, otherwise None.
        """
        return self.resource_paths.get(key, None)

    def construct_path(self, subpath: str) -> Path:
        """
        Construct a resource path.

        Parameters:
            subpath: A path.

        Returns:
            Path that starts with `root_directory` attribute.
        """
        return self.root_directory / subpath

    def mkdir(self, dir: Path) -> None:
        """
            Handles making directories if they don't exist.

            Parameters:
                dir: A directory that will be created (it always starts from the
                `root_directory`)

            Raises:
                OSError if it couldn't create the desired directory, however the
                error is re-raised so the caller handles it.
        """
        try:
            os.makedirs(dir, exist_ok=True)
        except OSError as e:
            print(f"Error while creating {e}")
            # Re-raise the error, make the caller handle it.
            raise
