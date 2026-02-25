from pathlib import Path
from typing import Dict


class ResourceManager:
    def __init__(self, root_directory: str, **kwargs):
        """
        Manages resources.

        Attributes:
            root_directory: A root directory, that will be used for path managing.
            resource_paths: Stores paths, all start with `root_directory`.
        """
        self.root_directory: Path = Path(root_directory)
        self.resource_paths: Dict[str, Path] = {
            k : self.construct_path(v) for k, v in kwargs.items()
        } 

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
