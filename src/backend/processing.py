import re
import pandas as pd
import fr_core_news_md

from methods import get_file_setting, load_raw_data, load_shop_data, get_dict_postal_geopoint, assign_group_name, remove_accents, cities_with_open_shop


file_setting = get_file_setting("settings.yml")
nlp_fr = fr_core_news_md.load()
# Specific stop words for city names in shop data.
nlp_fr.Defaults.stop_words |= {"l", "st", "saint"}

def preprocess(file_setting: dict) -> pd.DataFrame:
    # Data cleaning on the raw data.
    path_raw_data = file_setting.get("RAW_DATA")
    df_raw = load_raw_data(path_raw_data)
    # Keep only data from Google because there's no rating for reviews from facebook.
    df_google = df_raw[~(df_raw["Platform"] == "FACEBOOK")]
    # Keep only certains columns that are useful.
    cols_to_keep = ["Creation date", "Business Id", "Group name", "Address", "City", "Zipcode", "Content", "Response", "Rating"]
    df_google = df_google[cols_to_keep]
    # Remove tabs from city names.
    df_google["City"] = df_google["City"].str.strip()
    # Unify addresses (without street number).
    df_google["Address Without Number"] = df_google["Address"].apply(lambda x: re.sub(r"\d+\sb\s|^\d+-\d+\s|^\d+\s", "", x).title())
    # Imputation. Fill out missing group names from postal codes.
    df_google["Group name"] = df_google[["Group name", "Zipcode"]].apply(lambda x: assign_group_name(x["Zipcode"]) or x["Group name"], axis=1)

    # Data cleaning on the shop data.
    path_shop_data = file_setting.get("SHOP_DATA")
    df_shop = load_shop_data(path_shop_data)
    df_shop["LIB_MAGASIN"] = df_shop["LIB_MAGASIN"].str.replace(r"\d\s|\d", "", regex=True).str.title().str.strip()
    # Remove accents and tokenize city names in shop data.
    df_shop["Tokens Shop"] = df_shop["LIB_MAGASIN"].str.lower().apply(lambda x: [remove_accents(x.text) for x in nlp_fr(x) if not x.is_stop and not x.is_punct])
    df_city = df_google[["City", "Address Without Number"]].drop_duplicates()
    # Remove accents and tokenize city names in raw data.
    df_city["Tokens City"] = df_city["City"].str.lower().str.replace("-", " ").apply(lambda x: [remove_accents(x.text) for x in nlp_fr(x) if not x.is_stop and not x.is_punct])
    dict_shop = dict(zip(df_shop["LIB_MAGASIN"], df_shop["Tokens Shop"]))
    # If there's more than one word in common, we consider it as a match.
    df_city["Matched City in Shop Data"] = df_city["Tokens City"].apply(lambda x: [key for (key, value) in dict_shop.items() if len(set(x).intersection(value)) >= 1]).apply(lambda x: x[0] if len(x) > 0 else None)
    df_city["Is Open"] = df_city.apply(lambda x: True if x["Matched City in Shop Data"] and not any([y in x["Address Without Number"] for y in ["De Flandre", "De La Somme"]]) else (True if x["City"] in cities_with_open_shop else False), axis=1)
    df_city_matched = df_city[["City", "Address Without Number", "Matched City in Shop Data", "Is Open"]].reset_index(drop=True)
    return df_google, df_city_matched

def enrich(df_preprocessed: pd.DataFrame, df_city_matched: pd.DataFrame, file_setting: dict) -> pd.DataFrame:
    # Feature engineering. Arbitrarily gauge sentiments from ratings.
    df_preprocessed["Sentiment"] = df_preprocessed["Rating"].apply(lambda x: "Négatif" if x<3 else ("Neutre" if x==3 else "Positif"))
    # Feature engineering. Extract date from datetime.
    df_preprocessed["Date"] = df_preprocessed["Creation date"].dt.date
    # Feature engineering. Compare with shop data to know if the shops are in operation.
    addresses_with_open_shop = (df_city_matched[df_city_matched["Is Open"] == True]["Address Without Number"].values)
    df_preprocessed["Is Open"] = df_preprocessed["Address Without Number"].apply(lambda x: True if x in addresses_with_open_shop else False)
    # Feature engineering. Add GPS coordinates of the cities based on their postal codes.
    path_geo_data = file_setting.get("GEO_DATA")
    postal_geopoint = get_dict_postal_geopoint(path_geo_data)
    df_preprocessed["Latitude"] = df_preprocessed["Zipcode"].apply(lambda x: [geo_point[1] for postal_code, geo_point in postal_geopoint.items() if x in postal_code][0])
    df_preprocessed["Longitude"] = df_preprocessed["Zipcode"].apply(lambda x: [geo_point[0] for postal_code, geo_point in postal_geopoint.items() if x in postal_code][0])
    return df_preprocessed
