import requests
import json

class BCB:

    def __init__(self):

        self.url_std = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato={}&dataInicial={}&dataFinal={}"
    
    def get_data(self, code: str, format: str, start_date: str, end_date: str) -> json:
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

        url = self.url_std.format(code, format, start_date, end_date)
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch the data: {e}")
