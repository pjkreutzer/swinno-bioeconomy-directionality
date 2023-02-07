import argparse
from shutil import copy
from pathlib import Path
from src.utils import get_project_root
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True, help="Text file containing input ids.")

parser.add_argument("-l", "--lookup", required=True, help="Text file containing id lookup pairs.")

parser.add_argument("-s", "--source", type=Path, default=Path("/mnt/c/Users/ph8148kr/Lund University/Mathias Johansson - non_missing_source_materials/images").absolute(), help="Path for source of files.")

parser.add_argument("-d", "--destination", required=False, type=Path, help="Destination path in which to create destination dir")

args = vars((parser.parse_args()))

ROOT = get_project_root()


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

copy_sources()
