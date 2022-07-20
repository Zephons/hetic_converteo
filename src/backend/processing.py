import re
import pandas as pd

from methods import get_file_setting, load_raw_data, get_dict_postal_geopoint, assign_group_name


file_setting = get_file_setting("settings.yml")

def preprocess(path_raw_data: str) -> pd.DataFrame:
    df_raw = load_raw_data(path_raw_data)
    # Suppression. On ne garde que les commentaires google reviews.
    df_google = df_raw[~(df_raw["Platform"] == "FACEBOOK")]
    # Suppression. On crée un nouveau dataframe avec les colonnes qui nous intéressent.
    cols_to_keep = ["Creation date", "Business Id", "Group name", "Address", "City", "Zipcode", "Content", "Response", "Rating"]
    df_google = df_google[cols_to_keep]
    # Nettoyage. On enlève les tabulations dans les noms de ville.
    df_google["City"] = df_google["City"].str.strip()
    # Nettoyage. On unifie la forme des adresse (sans numéro).
    df_google["Address Without Number"] = df_google["Address"].apply(lambda x: re.sub(r"\d+\sb\s|^\d+-\d+\s|^\d+\s", "", x).title())
    # Imputation. On complète les Group name à partir des Zip code.
    df_google["Group name"] = df_google[["Group name", "Zipcode"]].apply(lambda x: assign_group_name(x["Zipcode"]) or x["Group name"], axis=1)
    return df_google

def enrich(df_preprocessed: pd.DataFrame, file_setting: dict) -> pd.DataFrame:
    path_geo_data = file_setting.get("GEO_DATA")
    postal_geopoint = get_dict_postal_geopoint(path_geo_data)
    df_preprocessed["Latitude"] = df_preprocessed["Zipcode"].apply(lambda x: [geo_point[1] for postal_code, geo_point in postal_geopoint.items() if x in postal_code][0])
    df_preprocessed["Longitude"] = df_preprocessed["Zipcode"].apply(lambda x: [geo_point[0] for postal_code, geo_point in postal_geopoint.items() if x in postal_code][0])
    # Feature engineering. On déduit les Sentiments à partir des Ratings.
    df_preprocessed["Sentiment"] = df_preprocessed["Rating"].apply(lambda x: "Négatif" if x<3 else ("Neutre" if x==3 else "Positif"))
    # Feature engineering. On extrait la date à partir de la date de création.
    df_preprocessed["Date"] = df_preprocessed["Creation date"].dt.date
    print(df_preprocessed)
    return df_preprocessed
