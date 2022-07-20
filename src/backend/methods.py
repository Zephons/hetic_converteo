import os
import json
import pandas as pd
from typing import List, Dict, Generator
from yaml import safe_load


def get_file_setting(path: str) -> dict:
    with open(path) as stream:
        settings = safe_load(stream)
        file_info = settings.get('FILE')
        flat_file_infos = list(_flatten_dict(file_info))
        # put all strings in lowercase in the nested list
        flat_lower_local_infos = [[element.lower() if element[0].isupper() else element for element in flat_local_info] for flat_local_info in flat_file_infos]
        file_setting = {}
        root_path = os.getcwd()
        for flat_lower_local_info in flat_lower_local_infos:
            # store the label in uppercase as key
            key = flat_lower_local_info[-2].upper()
            # remove the label (second to the last element) from path
            flat_lower_local_info.pop(-2)
            file_setting[key] = os.path.join(root_path, *flat_lower_local_info)
        return file_setting

def _flatten_dict(node_dict: dict, node_list: List = []) -> Generator[List[str], None, None]:
        """A helper method to flatten a nested dictionary to a nested list

        Parameters
        ----------
        node_dict : dict
            dictionary that contains all the file nodes
        node_list : List, optional
            list that contains file nodes

        Yields
        -------
        Generator[List[str], None, None]
            A generator that is a nested list which contains all the file paths
        """
        # flatten a nested dictionary to a list of lists
        for key, value in node_dict.items():
            yield from ([ node_list + [key, value]] if not isinstance(value, dict) else _flatten_dict(value, node_list + [key]))

def get_secrets(path: str) -> dict:
    if os.path.exists(path):
        with open(path) as stream:
            secrets = safe_load(stream)
        return secrets
    return None

# TODO If this function is launched for the Streamlit interface, @st.cache must be used to decorate this function.
def load_raw_data(path: str) -> pd.DataFrame:
    # On force le type de la colonne Zipcode en string.
    df_raw_data = pd.read_excel(path, header=[1], dtype={"Zipcode": str})
    return df_raw_data

def load_shop_data(path: str) -> pd.DataFrame:
    df_shop_data = pd.read_excel(path)
    return df_shop_data

def get_dict_postal_geopoint(path: str) -> Dict[str, List[float]]:
    with open(path) as stream:
        json_insee_postal = json.load(stream)
    dict_postal_geopoint = {element.get("fields").get("postal_code"): element.get("geometry").get("coordinates") for element in json_insee_postal}
    return dict_postal_geopoint

def assign_group_name(zip_code: str) -> str:
    # On trouve les Group name à partir des Zip code.
    zipcode_groupname = {
        "92800": "PARIS NORD",
        "91160": "PARIS SUD",
        "77340": "PARIS SUD",
        "95460": "PARIS NORD",
        "75019": "PARIS NORD",
        "95610": "PARIS NORD",
        "33700": "NOUVELLE AQUITAINE",
        "76000": "NORD",
        "49070": "OUEST"
    }
    return zipcode_groupname.get(zip_code)