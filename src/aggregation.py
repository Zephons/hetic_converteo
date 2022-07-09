import os
import pandas as pd
from sqlalchemy import create_engine

from process import preprocess, enrich


postgresql_uri = os.environ["DATABASE_URL"]

engine = create_engine(postgresql_uri.replace("postgres", "postgresql"))


# On force le type de la colonne Zipcode en string.
df = pd.read_excel("data/raw_datas_projet_M5D_Hetic.xlsx", header=[1], dtype={"Zipcode": str})
df_preprocessed = preprocess(df)
df_enriched = enrich(df_preprocessed)

# print(df_enriched["Creation date"].dt.date.nunique())

# Table pour les villes
df_city_address = df_enriched[["City", "Address Without Number"]].drop_duplicates().sort_values(by=["City", "Address Without Number"], ignore_index=True)
df_city_address.to_sql(name="city_address", con=engine, if_exists="replace")

# Table pour le pie chart Sentiment
df_pie_chart_sentiment = df_enriched.groupby(["City", "Address Without Number", "Sentiment"])["Sentiment"].count().reset_index(name="Count")
df_pie_chart_sentiment.to_sql(name="pie_chart_sentiment", con=engine, if_exists="replace")

