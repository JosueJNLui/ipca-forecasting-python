from ingestion.api import API
from ingestion.utils import Utils
from loguru import logger
from datetime import datetime
from ingestion.models import BCBJobParameters, SidraJobParameters
from ingestion.duck import DB
from ingestion.aws import list_bucket_objects

# import os
import fire
import boto3


AWS_PROFIILE = "profile"
AWS_ACCOUNT_ID = "11111111111111"
AWS_REGION = "us-east-2"
ENV = "dev"
S3_ASSETS_BUCKET = f"personal-projects-assets-{ENV}-{AWS_REGION}-{AWS_ACCOUNT_ID}"


def main() -> None:
    start_time = datetime.now()

    # Instanciando as classes desenvolvidas
    api = API()
    db = DB(AWS_PROFIILE, AWS_REGION)

    objects = list_bucket_objects(AWS_PROFIILE, AWS_REGION, S3_ASSETS_BUCKET, 'data_sources')

    # Iterando sobre os JSONs contendo as informações da fonte de dados
    for obj in objects:
        columns, results = db.query_from_s3(
            f"s3://{S3_ASSETS_BUCKET}/{obj}"
        )

        for row in results:

            if obj.split("/")[1].split(".")[0] == "bcb":
                params = BCBJobParameters(
                    start_date=row[columns.index("start_date")],
                    end_date=row[columns.index("end_date")],
                    format=row[columns.index("format")],
                    code=row[columns.index("code")],
                    table_name=row[columns.index("table_name")],
                )

                try: 
                    data = api.get_bcb_data(params)
                except:
                    continue
            
            if obj.split("/")[1].split(".")[0] == "sidra":
                params = SidraJobParameters(
                    code=row[columns.index("code")],
                    table_name=row[columns.index("table_name")],
                )

                try: 
                    data = api.get_sidra_data(params)
                    print(data)
                except:
                    continue
        
    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()
    logger.info(
        f"Job completed in {elapsed // 60} minutes and {elapsed % 60:.2f} seconds."
    )

if __name__ == "__main__":
    main()
