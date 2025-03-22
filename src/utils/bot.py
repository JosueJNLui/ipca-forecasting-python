import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import os
import shutil
import time
from utils import Excel, Utils

class WebBot:

    def __init__(self, download_folder_path: str, destiny_folder: str)  -> None:
        """

        Args:
            - download_folder_path (str):
            - destiny_folder(str):
        
        Returns:
            None
        """

        self.download_folder_path = download_folder_path
        self.destiny_folder = destiny_folder
        self.url = "https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos/precos-revenda-e-de-distribuicao-combustiveis/serie-historica-do-levantamento-de-precos"

    def get_driver(self):
        
        
        options = uc.ChromeOptions()
        prefs = {
            "download.default_directory": self.download_folder_path,
        }
        options.add_experimental_option("prefs", prefs)

        return uc.Chrome(
            options=options,
            headless=False,
            use_subprocess=False,
        )
    
    def get_reports(self):

        xpath_elements = {
            'from_2001_to_2012': ['//*[@id="parent-fieldname-text"]/ul[2]/li[1]/a', '//*[@id="parent-fieldname-text"]/ul[2]/li[1]/div/ul/li[1]/a'],
            'from_2013': ['//*[@id="parent-fieldname-text"]/ul[2]/li[2]/a', '//*[@id="parent-fieldname-text"]/ul[2]/li[2]/div/ul/li[1]/a']
        }

        for label, elements in xpath_elements.items():

            if os.path.exists(self.download_folder_path):
                shutil.rmtree(self.download_folder_path)
            os.mkdir(self.download_folder_path)

            driver = self.get_driver()
            driver.get(self.url)
            time.sleep(2)

            if driver.find_element(By.XPATH, '/html/body/div[5]/div'):
                driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div/div[2]/button[2]').click()

            driver.find_element(By.XPATH, elements[0]).click()
            time.sleep(2)
            
            driver.find_element(By.XPATH, elements[1]).click()
            time.sleep(2)

            driver.close()

            raw_file_path = os.path.join(self.download_folder_path, os.listdir(self.download_folder_path)[0])

            self.extract_data(raw_file_path, self.destiny_folder, label)
            shutil.rmtree(self.download_folder_path)

    @staticmethod
    def extract_data(excel_path: str, destiny_folder: str, filename: str):

        excel = Excel(excel_path)
        ws = excel.wb.worksheets[0]

        for row in ws.iter_cols():
            for cell in row:

                if cell.value == 'MÊS':
                    start_row = cell.row
                    break

        data = []

        header = {cell.column: Utils.process_text(cell.value) for cell in ws[start_row] if cell.value}

        for row in ws.iter_rows(start_row + 1,
                                ws.max_row, 
                                ws.min_column, 
                                len(header)
                            ):
            
            row_values = {}
            
            for i, cell in enumerate(row):
                row_values[header.get(i+1)] = str(cell.value)
            data.append(row_values)
        
        Utils.save_json(data, destiny_folder, filename)


if __name__ == '__main__':

    download_folder = '/home/josue-lui/dev/ipca-forecasting-python/temp-dir'
    destiny_folder = '/home/josue-lui/dev/ipca-forecasting-python/data'

    bot = WebBot(download_folder, destiny_folder)
    bot.get_reports()
