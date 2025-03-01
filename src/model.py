import polars as pl
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

from data_processing import read_data, pre_process_data, get_date_cols

class Model:

    def __init__(self, df: pl.DataFrame) -> None:
        self.df = df
    
    # def train_test_split(self, test_portion: float) -> list(pl.DataFrame):



    # def linear_regression(self, )

df = read_data('/home/josue-lui/dev/ipca-forecasting-python/data/historical_data.json')
df = pre_process_data(df, 'data', 'valor')
df = get_date_cols(df, 'data')

test_size = int(0.30 * len(df))

X_train  = (
    df[:-test_size]
    .select(pl.exclude("valor"))
)

y_train = (
    df[:-test_size]
    .select(pl.col("valor"))
)

X_test  = (
    df[-test_size:]
    .select(pl.exclude("valor"))
)

y_test = (
    df[-test_size:]
    .select(pl.col("valor"))
)

model = LinearRegression()
model.fit(X_train, y_train)


model.predict(X_test)

pred_df = pl.DataFrame({"label": y_test, "pred": np.array(model.predict(X_test)).flatten()})
