import json
import os
from unicodedata import normalize
import re
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl import load_workbook


class Utils:
    @staticmethod
    def save_json(json_obj: json, folder_path: str, filename: str) -> None:
        """
        Save JSON object in a specified path.

        Args:
            - json_obj (json): JSON object.
            - folder_path (str): Folder path to save the JSON.
            - filename (str): Desired destiny filename.

        Returns:
            None
        """

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        path = os.path.join(folder_path, f"{filename}.json")

        with open(path, "+w", encoding="utf-8") as f:
            json.dump(json_obj, f, ensure_ascii=False, indent=4)

    @staticmethod
    def read_json(json_path: str) -> json:
        """
        What function does

        Args:
            - json_path (str):

        Returns:
            str:
        """

        if not os.path.exists(json_path):
            with open(json_path, "w") as arquivo:
                arquivo.write("[]")

        with open(json_path, "r") as arquivo:
            return json.load(arquivo)

    @staticmethod
    def process_text(raw_text: str) -> str:
        """
        What function does

        Args:
            - raw_text (str):

        Returns:
            str:
        """

        text = normalize("NFKD", raw_text).encode("ASCII", "ignore").decode("ASCII")
        text = " ".join(text.strip().split())

        return re.sub("[^A-Za-z0-9 ]+", "", text).replace(" ", "_").lower()


class Excel:
    def __init__(self, path: str) -> None:
        """

        Args:
            - path (str):

        Returns
            None
        """

        self.path = path
        self.wb = load_workbook(path)

    def get_sheet_by_name(self, sheet_name: str):
        ws = self.wb[sheet_name]
        return ws

    @staticmethod
    def get_headers(worksheet: Worksheet) -> dict:
        headers = {cell.value: cell.column for cell in worksheet[1]}
        return headers

    def save_changes(self):
        self.wb.save(self.path)
