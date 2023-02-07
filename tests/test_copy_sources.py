import pytest
import shutil
from pathlib import Path
from collections import defaultdict

def copy_sources():
    input_path = Path(ROOT, args["input"])
    lookup_path = Path(ROOT, args["lookup"])
    source_path = args["source"]
    destination_path = args["destination"]
    
    input_ids = get_input_ids(input_path)
    source_names = get_source_names(lookup_path, input_ids)
    
    for id, sources in source_names.items():
        copy_files(id, sources, source_path, destination_path)

def get_input_ids(input_path):
    with open(input_path, "r") as f:
        return [line.strip()[:-3] for line in f.readlines()]

def get_source_names(lookup_path, input_ids):
    with open(lookup_path, "r") as f:
        lookup = defaultdict(list)
        for line in f:
            key, value = line.strip().split("|")
            lookup[key].append(value)
            
    return {k: lookup[k] for k in set(lookup).intersection(input_ids)}

def copy_files(id, sources, source_path, destination_path):
    for source in sources:
        files = list(source_path.glob(f"{source}*.*"))
        for f in files:
            dest = Path(destination_path, "images", f"{id}", f"{f.name}")

            if not dest.parent.exists():
                dest.mkdir(parents=True)
            
            try:
                copy(f, dest)
            except PermissionError:
                print(f"Error: Permission denied when copying {f} to {dest}")

        print(f"Copied {len(files)} images.")

def test_copy_sources():
    # Define the input, lookup, source and destination paths for testing
    input_file = Path("input.txt")
    lookup_file = Path("lookup.txt")
    source_path = Path("source/")
    destination_path = Path("destination/")
    
    # Create the input file
    with open(input_file, "w") as i:
        i.write("id1\nid2\nid3")

    # Create the lookup file
    with open(lookup_file, "w") as l:
        l.write("id1|file1\nid2|file2\nid3|file3")

    # Create the source directory and some dummy files
    source_path.mkdir()
    (source_path / "file1.txt").touch()
    (source_path / "file2.txt").touch()
    (source_path / "file3.txt").touch()

    # Define the args dictionary
    args = {
        "input": input_file,
        "lookup": lookup_file,
        "source": source_path,
        "destination": destination_path
    }

    # Call the copy_sources function
    copy_sources(args)
    
    # Assert that the destination directory was created
    assert destination_path.exists()

    # Assert that the subdirectories for each id were created
    for id in ["id1", "id2", "id3"]:
        subdir = destination_path / "images" / id
        assert subdir.exists()

    # Assert that the files were copied
    for id, filename in [("id1", "file1.txt"), ("id2", "file2.txt"), ("id3", "file3.txt")]:
        source_file = source_path / filename
        dest_file = destination_path / "images" / id / filename
        assert dest_file.exists()
        assert source_file.stat().st_size == dest_file.stat().st_size

    # Clean up
    shutil.rmtree(destination_path)
    shutil.rmtree(source_path)
    input_file.unlink()
    lookup_file.unlink()
