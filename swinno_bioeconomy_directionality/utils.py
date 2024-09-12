from pathlib import Path

def get_project_root():
    return Path(__file__).absolute().parent.parent

def format_table(df):
    # create a Styler object and set the wrapping style
    styler = df.style.set_properties(**{"width": "50em", "text-wrap": "break-word"})

    return styler

