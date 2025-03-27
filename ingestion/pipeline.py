from ingestion.api import API
from ingestion.utils import Utils
from loguru import logger
from datetime import datetime
from ingestion.models import BCBJobParameters, SidraJobParameters
import fire


def main() -> None:
    start_time = datetime.now()

    bcb_params = BCBJobParameters(
        start_date="01/01/1999",
        end_date="01/01/2025",
        format="json",
        code=10844,
        table_name="test_table",
        destination="local_path",
        s3_path="s3://bucket/path",
        aws_profile="dev",
    )

    sidra_params = SidraJobParameters(
        code="t/4093/n1/all/v/4099/p/all/c2/6794",
        table_name="test_table",
        destination="local_path",
        s3_path="s3://bucket/path",
        aws_profile="dev",
    )

    api = API()

    data_sources = {
        "bcb": {"ipca": 10844, "selic": 4390, "cambio": 10813, "m2": 1787, "icc": 4393},
        "sidra": {"desocupacao": "t/4093/n1/all/v/4099/p/all/c2/6794"},
    }

    for source, values in data_sources.items():
        for name, param in values.items():
            if source == "bcb":
                data = api.get_bcb_data(bcb_params)

            if source == "sidra":
                data = api.get_sidra_data(sidra_params)

            logger.info(f"Saving {name.upper()} as JSON file.")
            # Utils.save_json(data, "data", name)

    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()
    logger.info(
        f"Job completed in {elapsed // 60} minutes and {elapsed % 60:.2f} seconds."
    )


if __name__ == "__main__":
    main()
