import pandas as pd

def datetime_conversion(df, col, formats, output_col_name = 'datetime_col'):
    "Iterate through list of datetime formats to convert date string col to datetime"

    dates = pd.to_datetime(df[col], format= formats[0], errors='coerce')

    if len(formats) > 1:

        for format_type in formats[1:]:
            dates2 = pd.to_datetime(df[col], format=format_type, errors='coerce')
            dates = dates.combine_first(dates2)

    df[output_col_name] = dates

    return df