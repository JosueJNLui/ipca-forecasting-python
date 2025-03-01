import polars as pl
import os

def read_data(json_path: str) -> pl.DataFrame:

    if os.path.exists(json_path):
        df = pl.read_json(json_path)
        return df

def process_data(df: pl.DataFrame, date_col: str, value_col: str) -> pl.DataFrame:

    df = df.with_columns(
        pl.col(date_col).str.to_date("%d/%m/%Y"),
        pl.col(value_col).str.to_decimal()
    )

    return df
