from collections.abc import Callable, Sequence

import pandas as pd


def get_data_quality_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate a data quality report for the given DataFrame.

    Parameters:
    df (pd.DataFrame): The input DataFrame to analyze.

    Returns:
    pd.DataFrame: A DataFrame containing the data quality report.
    """
    # 1. Validate input
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame.")

    # 2. Calculate data quality metrics
    data_types = df.dtypes
    missing_counts = df.isna().sum()
    missing_pct = (df.isna().mean() * 100).round(2)
    unique_counts = df.nunique()
    
    # 3. Construct report DataFrame
    report = pd.DataFrame({
        'Data Type': data_types,
        'Missing Count': missing_counts,
        'Missing %': missing_pct,
        'Unique Values': unique_counts,
    })
    
    return report


def get_iqr_outliers(
    df: pd.DataFrame,
    columns: Sequence[str] | None = None,
    multiplier: float = 1.5,
) -> dict[str, pd.Series]:
    """Return IQR-based outlier masks for selected numeric columns.

    Args:
        df: Input DataFrame.
        columns: Numeric columns to inspect. If None, all numeric columns
            are selected.
        multiplier: IQR multiplier used to define the lower and upper bounds.

    Returns:
        A mapping from column name to a boolean outlier mask.

    Raises:
        TypeError: If ``df`` is not a DataFrame or a selected column is not
            numeric.
        ValueError: If ``multiplier`` is negative.
        KeyError: If a requested column does not exist.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")
    if multiplier < 0:
        raise ValueError("multiplier must be non-negative.")

    selected_columns = (
        df.select_dtypes(include="number").columns.tolist()
        if columns is None
        else list(columns)
    )
    missing_columns = sorted(set(selected_columns) - set(df.columns))
    if missing_columns:
        raise KeyError(f"Columns not found: {missing_columns}")

    outliers: dict[str, pd.Series] = {}
    for column in selected_columns:
        if not pd.api.types.is_numeric_dtype(df[column]):
            raise TypeError(f"Column '{column}' must be numeric.")

        values = df[column]
        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - multiplier * iqr
        upper_bound = q3 + multiplier * iqr
        outliers[column] = values.lt(lower_bound) | values.gt(upper_bound)

    return outliers


def get_numeric_domain_audit(
    df: pd.DataFrame,
    rules: Sequence[
        tuple[str, str, Callable[[pd.DataFrame], pd.Series] | pd.Series]
    ],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Audit numerical domain rules and return summary and invalid rows.

    Args:
        df: Input DataFrame to audit.
        rules: Tuples containing a feature-group name, rule description, and
            either a callable returning a boolean validity mask or an
            already-computed boolean Series.

    Returns:
        A tuple containing the domain summary and rows violating any rule.

    Raises:
        TypeError: If ``df`` is not a pandas DataFrame.
        ValueError: If a rule returns a mask with a different index.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    audit_rows: list[dict[str, object]] = []
    invalid_masks: dict[str, pd.Series] = {}

    for feature_group, description, rule in rules:
        mask = rule(df) if callable(rule) else rule
        if not isinstance(mask, pd.Series) or not mask.index.equals(df.index):
            raise ValueError(
                f"Rule '{feature_group}' must return a Series with the "
                "same index as the input DataFrame."
            )

        invalid_mask = ~mask.astype(bool)
        audit_rows.append(
            {
                "Feature group": feature_group,
                "Rule": description,
                "Invalid count": int(invalid_mask.sum()),
            }
        )
        invalid_masks[feature_group] = invalid_mask

    domain_audit = pd.DataFrame(
        audit_rows,
        columns=["Feature group", "Rule", "Invalid count"],
    )
    invalid_domain_mask: pd.Series = pd.DataFrame(
        invalid_masks, index=df.index
    ).any(axis=1)
    invalid_domain_rows = pd.DataFrame(df.loc[invalid_domain_mask])

    return domain_audit, invalid_domain_rows