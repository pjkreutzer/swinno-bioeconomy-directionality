import argparse
from pathlib import Path

from swinno_bioeconomy_directionality.file_utils import (
    copy_files,
    create_directory,
    get_input_ids,
    get_source_names,
)
from swinno_bioeconomy_directionality.utils import get_project_root

parser = argparse.ArgumentParser()
parser.add_argument(
    "-i", "--input", required=True, help="Text file containing input ids."
)

parser.add_argument(
    "-l",
    "--lookup",
    required=False,
    type=Path,
    default=None,
    help="Text file containing id lookup pairs.",
)

parser.add_argument(
    "--lookup-type",
    choices=["01", "02", "both"],  # Add more choices if needed
    default="both",
    help="Type or version of the lookup file.",
)

parser.add_argument(
    "-s",
    "--source",
    type=Path,
    default=Path(
        "/Users/research/OneDrive - Lund University/cloud-research/swinno-db/data/source_images"
    ).absolute(),
    help="Path for source of files.",
)

parser.add_argument(
    "-d",
    "--destination",
    required=False,
    type=Path,
    help="Destination path in which to create destination dir",
)

args = vars((parser.parse_args()))

ROOT = get_project_root()


if __name__ == "__main__":
    if not Path(ROOT, args["input"]).exists():
        raise FileNotFoundError(f"Input file {args['input']} does not exist.")
    else:
        input_path = Path(ROOT, args["input"])

        # Set the default lookup file(s) based on --lookup-type
    if args["lookup"] is None:
        if args["lookup_type"] == "both":
            args["lookup"] = [
                "notes/01-innovation_id_to_source_id.txt",
                "notes/02-innovation_id_to_source_id.txt",
            ]
        else:
            args["lookup"] = (
                f"notes/{args['lookup_type']}-innovation_id_to_source_id.txt"
            )

    if not Path(args["source"]).exists():
        source_path = Path(args["source"])
        raise NotADirectoryError(f"The directory '{source_path.name}' does not exist.")
    else:
        source_path = args["source"]

    destination_path = Path(ROOT, args["destination"])
    create_directory(destination_path)

    input_ids = get_input_ids(input_path)

    if isinstance(args["lookup"], list):
        # Handle the case where args["lookup"] is a list (both lookup files)
        for lookup_file in args["lookup"]:
            lookup_path = Path(ROOT, lookup_file)

            source_names = get_source_names(lookup_path, input_ids)

            copy_files(source_names, source_path, destination_path)

            if not lookup_path.exists():
                raise FileNotFoundError(f"Lookup file {lookup_path} does not exist.")
    else:
        # Handle the case where args["lookup"] is a single lookup file
        lookup_path = Path(ROOT, args["lookup"])
        source_names = get_source_names(lookup_path, input_ids)

        copy_files(source_names, source_path, destination_path)
        if not lookup_path.exists():
            raise FileNotFoundError(f"Lookup file {lookup_path} does not exist.")
