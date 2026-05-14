def get_data_file_path(filename):
    from pathlib import Path
    import os
    data_dir = Path(os.getenv("DATA_DIRECTORY", "/app/data"))
    return str(data_dir.joinpath(filename))
