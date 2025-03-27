import polars as pl
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.ensemble import RandomForestRegressor
from typing import Tuple
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
from data_processing import read_data, pre_process_data, date_features
import os
import json
from utils.utils import Utils
import random


class Model:
    def __init__(
        self, df: pl.DataFrame, test_portion: float, target_col: str, results_path: str
    ) -> None:
        self.X_train, self.y_train, self.X_test, self.y_test = self.train_test_split(
            df, test_portion, target_col
        )
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

    def forecast_model(self, model_name: str, selected_model) -> None:
        model = selected_model
        model.fit(self.X_train, np.ravel(self.y_train))

        self.y_predictions = model.predict(self.X_test)

        self.save_results(model_name)

    def save_results(self, model_name: str) -> dict:
        results = Utils.read_json(self.results_path)

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


HISTORICAL_DATA = (
    "/home/josue-lui/dev/ipca-forecasting-python/data/historical_data.json"
)
RESULTS_FILE = "/home/josue-lui/dev/ipca-forecasting-python/src/tests/results.json"
DATE_COL = "data"
TARGET_COL = "valor"
TEST_RATIO = 0.30

df = read_data(HISTORICAL_DATA)
df = pre_process_data(df, DATE_COL, TARGET_COL)
df = date_features(df, DATE_COL)

model = Model(df, TEST_RATIO, TARGET_COL, RESULTS_FILE)

models_dict = {
    "linear_regression": LinearRegression(),
    "xgboost_regressor": xgb.XGBRegressor(),
    "random_forest_regressor": RandomForestRegressor(random_state=42),
}

for k, v in models_dict.items():
    model.forecast_model(k, v)
