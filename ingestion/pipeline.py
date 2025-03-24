from ingestion.api import API
from ingestion.utils import Utils, SecretsManagerSecret

def main() -> None:

    # start_date = '01/01/1999'
    # end_date = '01/01/2025'

    # api = API()

    # data_sources = {

    #     'bcb': {
    #         'ipca': 10844,
    #         'selic': 4390,
    #         'cambio': 10813,
    #         'm2': 1787,
    #         'icc': 4393
    #     },
    #     'sidra': {
    #         'desocupacao': "t/4093/n1/all/v/4099/p/all/c2/6794"
    #     }
    # }

    # for source, values in data_sources.items():

    #     for name, param in values.items():
            
    #         if source == 'bcb':
    #             data = api.get_bcb_data(param, 'json', start_date, end_date)
            
    #         if source == 'sidra':
    #             data = api.get_sidra_data(param)
            
    #         Utils.save_json(data, 'data', name)

    client = SecretsManagerSecret('us-east-2', 'dev')
    print(client.client.list_buckets())
    

if __name__ == "__main__":
    main()
