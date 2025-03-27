from ingestion.models import (
    BCBJobParameters,
    SidraJobParameters,
    BCBResponseData,
    SidraRes,
)
from ingestion.api import API


def test_build_url_bcb():
    params = BCBJobParameters(
        start_date="01/01/1999",
        end_date="01/01/2025",
        format="json",
        code=1234,
        table_name="test_table",
        destination="local_path",
        s3_path="s3://bucket/path",
        aws_profile="dev",
    )

    api = API()
    url = api.build_url_bcb(params)

    expected_url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1234/dados?formato=json&dataInicial=01/01/1999&dataFinal=01/01/2025"

    assert url.strip() == expected_url.strip()


def test_build_url_sidra():
    params = SidraJobParameters(
        code="123456/test",
        table_name="test_table",
        destination="local_path",
        s3_path="s3://bucket/path",
        aws_profile="dev",
    )

    api = API()
    url = api.build_url_sidra(params)

    expected_url = "https://apisidra.ibge.gov.br/values/123456/test"

    assert url.strip() == expected_url.strip()
