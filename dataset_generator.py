from __future__ import annotations

import random
from typing import Literal

import numpy as np
import pandas as pd


RowStrategy = Literal["copy", "random"]


class DatasetGenerator:
    """
    Generate benchmark datasets from an existing CSV dataset.

    Supports:
    - Row scaling
    - Column scaling
    - Random data generation based on column types
    """


    def __init__(
        self,
        csv_path: str,
        seed: int = 42,
    ) -> None:

        self.df = pd.read_csv(csv_path)

        # Remove pandas exported index column
        if "Unnamed: 0" in self.df.columns:
            self.df = self.df.drop(columns=["Unnamed: 0"])

        self.seed = seed

        random.seed(seed)
        np.random.seed(seed)


    def generate(
        self,
        target_rows: int,
        target_columns: int | None = None,
        row_strategy: RowStrategy = "random",
    ) -> pd.DataFrame:
        """
        Generate dataset with requested size.

        Parameters
        ----------
        target_rows:
            Number of rows.

        target_columns:
            Number of columns.

        row_strategy:
            copy:
                Duplicate existing rows.

            random:
                Generate new values based on
                original column distributions.
        """


        if row_strategy == "copy":

            df = self._expand_rows(
                target_rows
            )

        elif row_strategy == "random":

            df = self._generate_rows(
                target_rows
            )

        else:

            raise ValueError(
                "row_strategy must be 'copy' or 'random'"
            )


        if target_columns is not None:

            df = self._adjust_columns(
                df,
                target_columns
            )


        return df.reset_index(drop=True)



    # ==========================================================
    # Row Generation
    # ==========================================================


    def _expand_rows(
        self,
        rows: int,
    ) -> pd.DataFrame:
        """
        Repeat existing rows.
        """

        repeat = (
            rows // len(self.df)
        ) + 1


        return (
            pd.concat(
                [self.df] * repeat,
                ignore_index=True
            )
            .iloc[:rows]
            .copy()
        )



    def _generate_rows(
        self,
        rows: int,
    ) -> pd.DataFrame:
        """
        Generate completely new rows
        according to column types.
        """

        data = {}


        for column in self.df.columns:

            data[column] = self._generate_column(
                self.df[column],
                rows
            )


        return pd.DataFrame(data)



    # ==========================================================
    # Column Generation
    # ==========================================================


    def _adjust_columns(
        self,
        df: pd.DataFrame,
        target_columns: int,
    ) -> pd.DataFrame:
        """
        Increase or decrease columns.
        """


        current_columns = df.shape[1]


        # Same size
        if target_columns == current_columns:
            return df


        # Remove columns
        if target_columns < current_columns:

            return (
                df.iloc[:, :target_columns]
                .copy()
            )


        # Add new columns

        source_index = 0


        while df.shape[1] < target_columns:


            source_column = self.df.columns[
                source_index % len(self.df.columns)
            ]


            new_column = (
                f"{source_column}_{source_index + 1}"
            )


            df[new_column] = self._generate_column(
                self.df[source_column],
                len(df)
            )


            source_index += 1


        return df



    # ==========================================================
    # Value Generation
    # ==========================================================


    def _generate_column(
        self,
        series: pd.Series,
        size: int,
    ) -> pd.Series:
        """
        Generate values according to dtype.
        """


        # Integer

        if pd.api.types.is_integer_dtype(series):

            return pd.Series(
                np.random.randint(
                    series.min(),
                    series.max() + 1,
                    size,
                )
            )


        # Float

        if pd.api.types.is_float_dtype(series):

            return pd.Series(
                np.random.uniform(
                    series.min(),
                    series.max(),
                    size,
                )
            )


        # Date

        if pd.api.types.is_datetime64_any_dtype(series):

            start = series.min()
            end = series.max()


            return pd.Series(
                pd.to_datetime(
                    np.random.randint(
                        start.value,
                        end.value,
                        size,
                    )
                )
            )



        # String / Category

        unique_values = (
            series
            .dropna()
            .unique()
        )


        if len(unique_values) == 0:

            return pd.Series(
                [None] * size
            )


        return pd.Series(
            np.random.choice(
                unique_values,
                size
            )
        )