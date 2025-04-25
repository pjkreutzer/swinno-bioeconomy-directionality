from pathlib import Path
import polars as pl

from swinno_bioeconomy_directionality.config import (
    RAW_DATA_DIR,
)
from swinno_bioeconomy_directionality.data_handling import process_data


def ensure_directory_exists(directory: Path):
    directory.mkdir(parents=True, exist_ok=True)


class DataLoader:
    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)

    def _validate_file(self, file_path):
        """
        Validate if a file exists.

        Args:
            file_path (Path): Path to the file.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File '{file_path}' does not exist.")

    def load_aggregated_collaborations(self, clean: bool = True) -> pl.DataFrame:
        file_path = self.data_dir / "aggregated_collaborations.csv"

        self._validate_file(file_path)

        aggregated_collaborations = pl.read_csv(
            file_path, schema_overrides={"sinno_id": pl.String}
        )

        if clean:
            aggregated_collaborations = aggregated_collaborations.pipe(
                process_data.clean_collaboration_data
            )

        return aggregated_collaborations

    def load_swinno(
        self, file_name: str = "swinno_data.csv", clean: bool = True, **kwargs
    ) -> pl.DataFrame:
        file_path = self.data_dir / file_name

        self._validate_file(file_path)

        return pl.read_csv(
            file_path,
            schema_overrides={
                "sinno_id": pl.String,
                "year": pl.Int64,
                "name": pl.String,
            },
        )

    def load_id_year_bioeconomy(self) -> pl.DataFrame:
        file_path = RAW_DATA_DIR / "cleaned_bioeconomy_query.csv"

        self._validate_file(file_path)

        id_year_bioeconomy = pl.read_csv(
            file_path,
            schema_overrides={
                "sinno_id": pl.String,
                "year": pl.Int64,
                "bioeconomy": pl.Int64,
            },
        )

        return id_year_bioeconomy

    def load_visions(self, file_name="bioeconomy_visions.csv"):
        file_path = self.data_dir / file_name

        self._validate_file(file_path)

        visions = pl.read_csv(
            file_path,
            schema_overrides={
                "sinno_id": pl.String,
                "year": pl.Int64,
                "bioeconomy_vision": pl.String,
            },
        )

        return visions.with_columns(
            pl.col("bioeconomy_vision").str.replace("Not Bioeconomy", "Vision Neutral")
        )
