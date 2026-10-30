from collections.abc import Sequence

import pandas as pd


def convert_to_category(
    df: pd.DataFrame,
    columns: Sequence[str],
) -> pd.DataFrame:
    """Convert selected DataFrame columns to pandas categorical dtype.

    Args:
        df: Input DataFrame.
        columns: Column names to convert.

    Returns:
        A copy of the DataFrame with the selected columns converted.

    Raises:
        TypeError: If ``df`` is not a pandas DataFrame.
        KeyError: If a requested column does not exist.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    column_names = list(columns)
    missing_columns = sorted(set(column_names) - set(df.columns))
    if missing_columns:
        raise KeyError(f"Columns not found: {missing_columns}")

    category_dtypes = {column: "category" for column in column_names}
    return df.copy().astype(category_dtypes)
