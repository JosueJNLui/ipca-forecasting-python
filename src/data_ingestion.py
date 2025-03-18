import requests
import json
from utils.utils import Utils
# from unicodedata import normalize
# import re

# def process_text(raw_text: str):
    
#     text = normalize('NFKD', raw_text).encode('ASCII', 'ignore').decode('ASCII')
#     text = ' '.join(text.strip().split())

#     return re.sub('[^A-Za-z0-9 ]+', '', text)

class API:

    def __init__(self) -> None:

        self.url_bcb = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato={}&dataInicial={}&dataFinal={}"
        self.url_sidra = "https://apisidra.ibge.gov.br/values/{}"
    
    def get_bcb_data(self, code: str, format: str, start_date: str, end_date: str) -> json:

        url = self.url_bcb.format(code, format, start_date, end_date)

        return self.get_request(url)

    def get_sidra_data(self, query_parameters: str) -> json:

        url = self.url_sidra.format(query_parameters)

        return self.get_request(url)

    def get_request(self, url: str) -> json:
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

        # url = self.url_std.format(code, format, start_date, end_date)
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch the data: {e}")

if __name__ == '__main__':

    start_date = '01/01/1999'
    end_date = '01/01/2025'

    api = API()

    bcb_codes = {
        'ipca': 10844,
        'selic': 4390,
        'cambio': 10813,
        'm2': 1787,
        'icc': 4393
    }

    sidra_query_parameters = {
        'desocupacao': "t/4093/n1/all/v/4099/p/all/c2/6794"
    }


    # for name, code in bcb_codes.items():

    #     data = api.get_bcb_data(code, 'json', start_date, end_date)
        
    #     Utils.save_json(data, '../data', name)

    for name, param in sidra_query_parameters.items():

        data = api.get_sidra_data(param)

        # processed_data = [
        #     {k: process_text(v) if isinstance(v, str) else v 
        #      for k, v in d.items()}
        #      for d in data
        # ]


        
    Utils.save_json(data, '../data', name)