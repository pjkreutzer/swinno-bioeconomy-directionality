import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal
from src.swinno_helpers import split_cols

test_input_df = pd.DataFrame({"A": ["1 2", np.nan, "0", "1 2"]})

expected_result_df = pd.DataFrame(
    {"A_0": ["1", np.nan, "0", "1"], "A_1": ["2", np.nan, np.nan, "2"]}
)


def test_df_equal():
    function_result = split_cols(test_input_df, "A", sep=" ")
    assert_frame_equal(expected_result_df, function_result, check_dtype=False)
