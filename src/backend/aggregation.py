import os
import pandas as pd
from sqlalchemy import create_engine

from methods import get_file_setting, get_secrets
from processing import preprocess, enrich


file_setting = get_file_setting("settings.yml")
path_raw_data = file_setting.get("RAW_DATA")
secrets = get_secrets(file_setting.get("SECRETS"))
postgresql_uri = os.environ.get("DATABASE_URL") or secrets.get("POSTGRESQL").get("URI")
engine = create_engine(postgresql_uri.replace("postgres", "postgresql"))

df_preprocessed, df_city_matched = preprocess(file_setting)
df_enriched = enrich(df_preprocessed, df_city_matched, file_setting)

# Create SQL Table for the filters (city, address and date).
df_city_address = df_enriched[["City", "Address Without Number", "Date"]].drop_duplicates().sort_values(by=["City", "Address Without Number", "Date"], ignore_index=True)
df_city_address.to_sql(name="filters", con=engine, if_exists="replace")

# Create SQL Table for the pie chart Sentiment.
df_pie_chart_sentiment = df_enriched.groupby(["City", "Address Without Number", "Date", "Sentiment"])["Sentiment"].count().reset_index(name="Count")
df_pie_chart_sentiment.to_sql(name="pie_chart_sentiment", con=engine, if_exists="replace")

# Create SQL Table for the KPIs and the map: number of comments, number of ratings, average rating, latitude and longitude of the cities.
groupby_filter = df_enriched.groupby(["City", "Address Without Number", "Is Open", "Date", "Latitude", "Longitude"])
df_nb_comments = groupby_filter["Content"].count().reset_index(name="Number of Comments")
df_nb_ratings = groupby_filter["Rating"].count().reset_index(name="Number of Ratings")
df_rating = groupby_filter["Rating"].mean().round(2).reset_index(name="Average Rating")
df_metrics_map = pd.concat([df_nb_comments, df_nb_ratings[["Number of Ratings"]], df_rating[["Average Rating"]]], axis=1)
# lower_tertile_point = df_map["Average Rating"].quantile(0.33)
# upper_tertile_point = df_map["Average Rating"].quantile(0.66)
# df_map["Rating Tertile"] = df_map["Average Rating"].apply(lambda x: f"Moins de {lower_tertile_point}" if x < lower_tertile_point else (f"Plus de {upper_tertile_point}" if x > upper_tertile_point else f"Entre {lower_tertile_point} et {upper_tertile_point}"))
df_metrics_map.to_sql(name="metrics_map", con=engine, if_exists="replace")
