from pathlib import Path
from collections import defaultdict
from shutil import copy


def create_directory(directory_path):
    if not directory_path.is_dir():
        directory_path.mkdir(parents=True)
        


def get_input_ids(input_path):
    """
    Reads a list of input IDs from a file and returns a list of the IDs with the file extension removed.

    Args:
        input_path (str): The path to the input file.

    Returns:
        list: A list of input IDs.

    Raises:
        FileNotFoundError: If the input file does not exist.
        Exception: If an error occurs when opening or reading the input file.
    """
    try:
        with open(input_path, "r") as f:
            return [line.strip()[:-3] for line in f.readlines()]
    except FileNotFoundError:
        print(f"Error: input file {input_path} not found.")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []


def get_source_names(lookup_path, input_ids):
    """
    Reads a lookup file and returns a dictionary of source names for the given input IDs.

    Args:
        lookup_path (str): The path to the lookup file.
        input_ids (list): A list of input IDs.

    Returns:
        dict: A dictionary of source names for the given input IDs.

    Raises:
        FileNotFoundError: If the lookup file does not exist.
        Exception: If an error occurs when opening or reading the lookup file.
    """
    with open(lookup_path, "r") as f:
        lookup = defaultdict(list)
        for line in f:
            try:
                key, value = line.strip().split("|")
                lookup[key].append(value)
            except ValueError:
                print(f"Warning: invalid line in lookup file: {line.strip()}")

    return {k: lookup[k] for k in set(lookup).intersection(input_ids)}

def copy_files(source_links: dict, source_dir: Path, destination_dir: Path):
    """
    Copies files from the source directory to the destination directory based on the provided source links.

    Args:
        source_links (dict): A dictionary mapping sinno_ids to lists of image prefixes.
        source_dir (Path): The path to the source directory.
        destination_dir (Path): The path to the destination directory.

    Raises:
        ValueError: If the source directory does not exist.

    Returns:
        None
    """
    if not source_dir.is_dir():
        raise ValueError("Source directory does not exist.")
    
    for sinno_id in source_links.keys():
        destination_path = destination_dir / sinno_id
        create_directory(destination_path)
        
        for image_prefix in source_links[sinno_id]:
            files = list(Path(source_dir).glob(f"{image_prefix}*"))
            
            for f in files:
                if f.is_file():
                    try:
                        copy(f, destination_path / f.name)
                    except PermissionError:
                        print(f"Error: Permission denied when copying {f} to {destination_path}")
        
        print(f"Copied {len(files)} images for sinno_id {sinno_id}.")

