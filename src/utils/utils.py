import json
import os

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

        with open(path, '+w') as f:
            json.dump(json_obj, f)
