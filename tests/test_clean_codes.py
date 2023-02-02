import pandas as pd
from pandas.testing import assert_frame_equal
from  src.categorization_helpers import *

input_df = pd.DataFrame(
    {"id": [1, 2, 3, 4, 5], "codes": ["A 0", "   1,23", "A,1", "ABC", " 1, 2, 0"]}
)

def test_letter_to_code():

    expected_df = pd.DataFrame(
        {"id": [1, 2, 3, 4, 5], "codes": ["1 0", "   1,23", "1,1", "123", " 1, 2, 0"]}
    )

    output_df = replace_letters_codes(input_df, "codes")

    assert_frame_equal(expected_df, output_df, check_names=False)


def test_clean_codes_1_digit():

    expected_df = pd.DataFrame(
        {"id": [1, 2, 3, 4, 5], "codes": ["1,0", "1,2,3", "1,1", "1,2,3", "1,2,0"]}
    )

    replaced_letters = replace_letters_codes(input_df, "codes")

    output_df = clean_codes(replaced_letters, code_digits=1, col="codes")

    assert expected_df["codes"].all() == output_df["codes"].all()


def test_clean_codes_3_digit():

    input_df = pd.DataFrame(
        {"id": [1, 2, 3], "codes": ["112322,0", "1230", "123123"]}
    )
    expected_df = pd.DataFrame(
        {"id": [1, 2, 3], "codes": ["112,322,0", "123,0", "123, 123"]}
    )

    replaced_letters = replace_letters_codes(input_df, "codes")

    output_df = clean_codes(replaced_letters, code_digits=3, col="codes")

    assert expected_df["codes"].all() == output_df["codes"].all()

def test_clean_codes_int_handling():

    input_df = pd.DataFrame(
        {"id": [1, 2, 3], "codes": ["112322,0", "1230", 123123]}
    )
    expected_df = pd.DataFrame(
        {"id": [1, 2, 3], "codes": ["112,322,0", "123,0", "123, 123"]}
    )

    replaced_letters = replace_letters_codes(input_df, "codes")

    output_df = clean_codes(replaced_letters, code_digits=3, col="codes")

    assert expected_df["codes"].all() == output_df["codes"].all()