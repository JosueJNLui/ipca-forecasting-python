import requests
import json
from utils.utils import Utils

class API:

    def __init__(self) -> None:

        self.url_bcb = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato={}&dataInicial={}&dataFinal={}"
        self.url_sidra = "https://apisidra.ibge.gov.br/values/{}"
    
    def get_bcb_data(self, code: str, format: str, start_date: str, end_date: str) -> json:

        url = self.url_bcb.format(code, format, start_date, end_date)

        return self.get_request(url)

    def get_sidra_data(self, query_parameters: str) -> json:

        url = self.url_sidra.format(query_parameters)

        raw_data = self.get_request(url)
        
        header = {k: Utils.process_text(v) for k, v in raw_data[0].items()}
        data = []

        for row in raw_data[1:]:

            raw_values = {}

            for k, v in row.items():
                raw_values[header.get(k)] = v
            
            data.append(raw_values)
        
        return data


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

    data_sources = {

        'bcb': {
            'ipca': 10844,
            'selic': 4390,
            'cambio': 10813,
            'm2': 1787,
            'icc': 4393
        },
        'sidra': {
            'desocupacao': "t/4093/n1/all/v/4099/p/all/c2/6794"
        }
    }

    for source, values in data_sources.items():

        for name, param in values.items():
            
            if source == 'bcb':
                data = api.get_bcb_data(param, 'json', start_date, end_date)
            
            if source == 'sidra':
                data = api.get_sidra_data(param)
            
            Utils.save_json(data, '../data', name)
