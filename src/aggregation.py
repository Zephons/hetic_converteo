import os
import pandas as pd
from sqlalchemy import create_engine

from process import load_raw_data, preprocess, enrich


postgresql_uri = os.environ["DATABASE_URL"]
path_raw_data = os.path.join("data", "raw_datas_projet_M5D_Hetic.xlsx")
engine = create_engine(postgresql_uri.replace("postgres", "postgresql"))

df_raw_data = load_raw_data(path_raw_data)
df_preprocessed = preprocess(df_raw_data)
df_enriched = enrich(df_preprocessed)

# Table pour les villes, les adresses et les dates.
df_city_address = df_enriched[["City", "Address Without Number", "Date"]].drop_duplicates().sort_values(by=["City", "Address Without Number", "Date"], ignore_index=True)
df_city_address.to_sql(name="city_address_date", con=engine, if_exists="replace")

# Table pour le pie chart Sentiment.
df_pie_chart_sentiment = df_enriched.groupby(["City", "Address Without Number", "Date", "Sentiment"])["Sentiment"].count().reset_index(name="Count")
df_pie_chart_sentiment.to_sql(name="pie_chart_sentiment", con=engine, if_exists="replace")

# Table pour les metriques : nombre d'avis, nombre de rating, rating moyen.
groupby_filter = df_enriched.groupby(["City", "Address Without Number", "Date"])
df_nb_comments = groupby_filter["Content"].count().reset_index(name="Number of Comments")
df_nb_ratings = groupby_filter["Rating"].count().reset_index(name="Number of Ratings")
df_rating = groupby_filter["Rating"].mean().round(2).reset_index(name="Average Rating")
df_metrics = pd.concat([df_nb_comments, df_nb_ratings[["Number of Ratings"]], df_rating[["Average Rating"]]], axis=1)
df_metrics.to_sql(name="metrics", con=engine, if_exists="replace")

