import os
import re
import pandas as pd

from methods import assign_group_name


postgresql_uri = os.environ["DATABASE_URL"]

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    # Suppression. On ne garde que les commentaires google reviews.
    df_google = df[~(df["Platform"] == "FACEBOOK")]
    # Suppression. On crée un nouveau dataframe avec les colonnes qui nous intéressent.
    cols_to_keep = ["Creation date", "Business Id", "Group name", "Address", "City", "Zipcode", "Content", "Response", "Rating"]
    df_google = df_google[cols_to_keep]
    # Nettoyage. On enlève les tabulations dans les noms de ville.
    df_google["City"] = df_google["City"].str.strip()
    # Imputation. On complète les Group name à partir des Zip code.
    df_google["Group name"] = df_google[["Group name", "Zipcode"]].apply(lambda x: assign_group_name(x["Zipcode"]) or x["Group name"], axis=1)
    return df_google

def enrich(df_preprocessed: pd.DataFrame) -> pd.DataFrame:
    # Feature engineering. On déduit les Sentiments à partir des Ratings.
    df_preprocessed["Sentiment"] = df_preprocessed["Rating"].apply(lambda x: "Negative" if x<3 else ("Neutral" if x==3 else "Positive"))
    # Feature engineering. On merge la ville et l"adresse pour désigner le magasin.
    df_preprocessed["Shop"] = df_preprocessed[["City", "Address"]].apply(lambda x: ", ".join([x["City"], re.sub(r"\d+\sb\s|^\d+-\d+\s|^\d+\s", "", x["Address"]).title()]), axis=1)
    return df_preprocessed
