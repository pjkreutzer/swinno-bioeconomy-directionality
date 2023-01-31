import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal
from src.swinno_helpers import melt_table


test_input_df = pd.DataFrame(
    {
        "ID": [1, 2, 3, 4],
        "A_0": ["1", np.nan, "0", "1"],
        "A_1": ["2", np.nan, np.nan, "2"],
    }
)

expected_result = pd.DataFrame(
    {
        "ID": [1, 1, 2, 2, 3, 3, 4, 4],
        "B": ["1", "2", np.nan, np.nan, "0", np.nan, "1", "2"],
    }
)


def test_melt_tables():
    function_result = melt_table(
        test_input_df, id_vars="ID", col_start="A", value_name="B"
    )
    assert_frame_equal(expected_result, function_result)
