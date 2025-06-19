import os
import datetime
from typing import List, Dict, Optional


def save_dict_list_as_file(data_dict_list: List[Dict], dir_path: str) -> Optional[str]:
    if not data_dict_list:
        return None

    os.makedirs(dir_path, exist_ok=True)

    filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
    filepath = os.path.join(dir_path, filename)

    try:
        with open(filepath, "w", encoding="utf-8") as file:
            for data_dict in data_dict_list:
                for column, content in data_dict.items():
                    file.write(f"{column}: {content}\n")
                file.write("\n")  # 각 딕셔너리 구분

        return os.path.abspath(filepath)
    except Exception as e:
        print(f"[save_dict_list_as_file] Error: {e}")
        return None
