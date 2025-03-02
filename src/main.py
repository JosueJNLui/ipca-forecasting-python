from utils.utils import Utils
from data_ingestion import BCB


bcb = BCB()

data = bcb.get_data('10844', 'json', '01/01/1999', '01/01/2025')

Utils.save_json(data, '../data', 'historical_data')
