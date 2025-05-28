import polars as pl
from typing import Tuple
import numpy as np
import json
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
import os
import matplotlib.pyplot as plt


class Model:
    def __init__(
        self, df: pl.DataFrame, test_portion: float, target_col: str, results_path: str
    ) -> None:
        self.X_train, self.y_train, self.X_test, self.y_test = self.train_test_split(
            df, test_portion, target_col
        )
        self.df = df
        self.y_predictions = None
        self.results_path = results_path

    def train_test_split(
        self, df: pl.DataFrame, test_portion: float, target_col: str
    ) -> Tuple[pl.DataFrame, pl.DataFrame, pl.DataFrame, pl.DataFrame]:
        if not 0 < test_portion < 1:
            raise ValueError("test portion musut be between 0 and 1.")

        if target_col not in df.columns:
            raise ValueError(f"Target column {target_col} not found in DataFrame")

        test_size = int(test_portion * len(df))

        X_train = df[:-test_size].select(pl.exclude(target_col))
        y_train = df[:-test_size].select(pl.col(target_col))
        X_test = df[-test_size:].select(pl.exclude(target_col))
        y_test = df[-test_size:].select(pl.col(target_col))

        return X_train, y_train, X_test, y_test

    def forecast_model(
        self, model_name: str, selected_model, cols_to_remove: list[str]
    ) -> None:
        model = selected_model
        model.fit(
            self.X_train.select(pl.exclude(cols_to_remove)), np.ravel(self.y_train)
        )

        self.y_predictions = model.predict(
            self.X_test.select(pl.exclude(cols_to_remove))
        )

        self.save_results(model_name)
        self.plot(model_name)

    def save_results(self, model_name: str) -> dict:
        results = read_json(self.results_path)

        info = {
            "model": model_name,
            "mae": mean_absolute_error(self.y_test, self.y_predictions),
            "rmse": root_mean_squared_error(self.y_test, self.y_predictions),
            "r2": r2_score(self.y_test, self.y_predictions),
        }

        if info not in results:
            results.append(info)

        with open(self.results_path, "w") as arquivo:
            json.dump(results, arquivo, indent=4)

    def plot(self, model_name: str):
        df = self.df.select(["month_year", "ipca_value"])

        y_pred = pl.Series("y_pred", self.y_predictions)
        forecast_df = self.X_test.with_columns(y_pred).select(["month_year", "y_pred"])

        df = df.join(forecast_df, on=["month_year"], how="left")

        df = df.with_columns([pl.col("month_year").str.strptime(pl.Date, "%Y-%m")])
        pdf = df.to_pandas()

        # Plotting
        plt.figure(figsize=(8, 5))
        plt.plot(pdf["month_year"], pdf["y_pred"], label='y_pred', color='black')
        plt.plot(pdf["month_year"], pdf["ipca_value"], label='ipca_value', color='green')

        # Formatting
        print()
        plt.xlabel("Month-Year")
        plt.ylabel("Value")
        plt.title("Forecast vs IPCA")
        plt.legend()
        plt.grid(True)

        # Save to PNG
        plt.savefig(f"{model_name}.png", dpi=300)
        plt.close()


def read_json(json_path: str) -> json:
    """
    What function does

    Args:
        - json_path (str):

    Returns:
        str:
    """

    if not os.path.exists(json_path):
        with open(json_path, "w") as arquivo:
            arquivo.write("[]")

    with open(json_path, "r") as arquivo:
        return json.load(arquivo)
