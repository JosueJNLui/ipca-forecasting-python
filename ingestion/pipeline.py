from ingestion.api import API
# from ingestion.utils import Utils
from loguru import logger
from datetime import datetime
from ingestion.models import BCBJobParameters, SidraJobParameters, IngestionJobParameters
from ingestion.duck import DB
from ingestion.aws import list_bucket_objects
import pyarrow as pa
import fire

def main(params: IngestionJobParameters) -> None:
    start_time = datetime.now()

    ENV = params.env
    AWS_REGION = params.aws_region
    AWS_ACCOUNT_ID = params.aws_account_id
    AWS_PROFIILE = params.aws_profile

    S3_ASSETS_BUCKET = f"personal-projects-assets-{ENV}-{AWS_REGION}-{AWS_ACCOUNT_ID}"
    S3_LANDING_BUCKET = f"personal-projects-landing-{ENV}-{AWS_REGION}-{AWS_ACCOUNT_ID}"

    # Instanciando as classes desenvolvidas
    api = API()
    db = DB(AWS_PROFIILE, AWS_REGION)

    DATA_SOURCES = {
        "bcb": {
            "param_class": BCBJobParameters,
            "api_method": api.get_bcb_data,
            "required_fields": ["start_date", "end_date", "format", "code", "table_name"]
        },
        "sidra": {
            "param_class": SidraJobParameters,
            "api_method": api.get_sidra_data,
            "required_fields": ["code", "table_name"]
        }
    }

    bucket_objects = list_bucket_objects(AWS_PROFIILE, AWS_REGION, S3_ASSETS_BUCKET, 'data_sources')

    # Iterando sobre os JSONs contendo as informações da fonte de dados
    for object_path in bucket_objects:

        file_key = object_path.split("/")[1]
        object = file_key.split(".")[0]

        if object not in DATA_SOURCES:
            continue

        columns, results = db.query_from_s3(f"{S3_ASSETS_BUCKET}/{object_path}")
        column_index = {col: idx for idx, col in enumerate(columns)}
        config = DATA_SOURCES[object]

        for row in results:

            param_args = {
                field: row[column_index[field]] for field in config["required_fields"]
            }

            try:

                params = config["param_class"](**param_args)
                data = config["api_method"](params)
                table_name = param_args["table_name"]

                arrow_table = pa.Table.from_pylist(data)

                db.write_json_to_s3(data, S3_LANDING_BUCKET, f'ipca-project/{table_name}')

            except Exception as e:
                continue
        
    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()
    logger.info(
        f"Job completed in {elapsed // 60} minutes and {elapsed % 60:.2f} seconds."
    )

if __name__ == "__main__":
    # print(**kwargs)
    fire.Fire(lambda **kwargs: main(IngestionJobParameters(**kwargs)))
