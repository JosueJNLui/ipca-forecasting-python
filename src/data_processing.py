import polars as pl
import os

def read_data(json_path: str) -> pl.DataFrame:

    if os.path.exists(json_path):
        df = pl.read_json(json_path)
        return df

def pre_process_data(df: pl.DataFrame, date_col: str, value_col: str) -> pl.DataFrame:

    df = df.with_columns(
        pl.col(date_col).str.to_date("%d/%m/%Y"),
        pl.col(value_col).str.to_decimal()
    )

    return df

def get_date_cols(df: pl.DataFrame, date_col: str) -> pl.DataFrame:

    df = df.with_columns(
        year = pl.col(date_col).dt.year(),
        month = pl.col(date_col).dt.month()
    )

    return df.select(pl.exclude(date_col))
