import requests
import json
from ingestion.utils import Utils
from loguru import logger
from ingestion.models import BCBJobParameters, SidraJobParameters
import time


class API:
    def __init__(self) -> None:
        self.url_bcb = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato={}&dataInicial={}&dataFinal={}"
        self.url_sidra = "https://apisidra.ibge.gov.br/values/{}"

    def build_url_bcb(self, params: BCBJobParameters) -> str:
        return self.url_bcb.format(
            params.code, params.format, params.start_date, params.end_date
        )

    def build_url_sidra(self, params: SidraJobParameters) -> str:
        return self.url_sidra.format(params.code)

    def get_bcb_data(self, params: BCBJobParameters) -> json:
        url = self.build_url_bcb(params)
        return self.get_request(url)

    def get_sidra_data(self, params: SidraJobParameters) -> json:
        url = self.build_url_sidra(params)

        raw_data = self.get_request(url)

        header = {k: Utils.process_text(v) for k, v in raw_data[0].items()}
        data = []

        for row in raw_data[1:]:
            raw_values = {}

            for k, v in row.items():
                raw_values[header.get(k)] = v

            data.append(raw_values)

        return data

    def get_request(self, url: str, trial: int = 1) -> json:
        """
        Get data from BCB API - Temporal Series System Manager.

        Args:
            - code (str): The series code.
            - format (str): The response format (e.g., 'json').
            - start_date (str): The start date in 'dd/MM/yyyy' format.
            - end_date (str): The end date in 'dd/MM/yyyy' format.

        Returns:
            json: The JSON response from the API.
        """
        
        while trial <=3:

            try:
                response = requests.get(url)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                logger.error(f"Failed for the {trial} time to fetch the data. Waiting 02 seconds to try it again")
                time.sleep(2)
                self.get_request(url, trial+1)
                # raise

        logger.error(f"Failed to fetch the data from {url} endpoint: {e}")
        raise
