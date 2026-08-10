import time

import pandas as pd
import polars as pl


def _time(fn) -> float:
    start = time.perf_counter()
    fn()
    return time.perf_counter() - start


def run_pandas_ops(df: pd.DataFrame) -> dict:
    """
    Time a handful of common DataFrame operations on pandas.
    """

    times = {}

    # Threshold computed once outside the timed block, so the
    # filter timing measures only the filter itself.
    threshold = df["Sales_Amount"].mean()

    times["groupby_mean"] = _time(
        lambda: df.groupby("Product_Category")["Sales_Amount"].mean()
    )

    times["filter"] = _time(
        lambda: df[df["Sales_Amount"] > threshold]
    )

    times["sort"] = _time(
        lambda: df.sort_values("Sales_Amount")
    )

    times["nunique"] = _time(
        lambda: df.nunique()
    )

    times["describe"] = _time(
        lambda: df.describe()
    )

    return times


def run_polars_ops(df: pl.DataFrame) -> dict:
    """
    Time the same operations on polars, for a like-for-like comparison.
    """

    times = {}

    threshold = df["Sales_Amount"].mean()

    times["groupby_mean"] = _time(
        lambda: df.group_by("Product_Category").agg(
            pl.col("Sales_Amount").mean()
        )
    )

    times["filter"] = _time(
        lambda: df.filter(pl.col("Sales_Amount") > threshold)
    )

    times["sort"] = _time(
        lambda: df.sort("Sales_Amount")
    )

    times["nunique"] = _time(
        lambda: df.select(pl.all().n_unique())
    )

    times["describe"] = _time(
        lambda: df.describe()
    )

    return times