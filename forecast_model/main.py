from forecast_model.models import ForecastJobParameters
from forecast_model.utils import Model
import fire
from datetime import datetime
from ingestion.duck import DB
import polars as pl
from sklearn.linear_model import LinearRegression
import xgboost as xgb
from sklearn.ensemble import RandomForestRegressor


def main(params: ForecastJobParameters) -> None:
    start_time = datetime.now()

    ENV = params.env
    AWS_REGION = params.aws_region
    AWS_ACCOUNT_ID = params.aws_account_id
    AWS_PROFIILE = params.aws_profile

    # Instanciando as classes desenvolvidas
    db = DB(AWS_PROFIILE, AWS_REGION)

    S3_SILVER_BUCKET = f"personal-projects-silver-{ENV}-{AWS_REGION}-{AWS_ACCOUNT_ID}"
    object_path = "ipca-project/ipca_historical_data/*/*.parquet"

    columns, results = db.query_from_s3(f"{S3_SILVER_BUCKET}/{object_path}")

    df = pl.DataFrame(results, schema=columns, orient="row")

    df = df.with_columns(
        [
            pl.col(col).cast(pl.Float64)
            for col, dtype in zip(df.columns, df.dtypes)
            if dtype == pl.Decimal
        ]
    )

    df = df.sort(pl.col("month_year"))

    model = Model(
        df,
        0.30,
        "ipca_value",
        "/workspaces/ipca-forecasting-python/forecast_model/results.json",
    )

    models_dict = {
        "linear_regression": LinearRegression(),
        "xgboost_regressor": xgb.XGBRegressor(),
        "random_forest_regressor": RandomForestRegressor(random_state=42),
    }

    for k, v in models_dict.items():
        model.forecast_model(k, v, ["date", "month_year"])

    # print(df.schema)


if __name__ == "__main__":
    fire.Fire(lambda **kwargs: main(ForecastJobParameters(**kwargs)))
