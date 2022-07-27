import os
import pandas as pd
from sqlalchemy import create_engine

from methods import get_file_setting, get_secrets, load_nlp_data
from processing import preprocess, enrich


file_setting = get_file_setting("settings.yml")
path_raw_data = file_setting.get("RAW_DATA")
secrets = get_secrets(file_setting.get("SECRETS"))
postgresql_uri = os.environ.get("DATABASE_URL") or secrets.get("POSTGRESQL").get("URI")
engine = create_engine(postgresql_uri.replace("postgres", "postgresql"))

df_preprocessed, df_city_matched = preprocess(file_setting)
df_enriched = enrich(df_preprocessed, df_city_matched, file_setting)

# Create SQL table for the filters (city, address and first day of the month).
df_city_address = df_enriched[["City", "Address Without Number", "Month"]].drop_duplicates().sort_values(by=["City", "Address Without Number", "Month"], ignore_index=True)
df_city_address.to_sql(name="filters", con=engine, if_exists="replace")

# Create SQL table for the informations of the shops.
df_shop_info = df_enriched[["City", "Address Without Number", "Group Name", "Is Open"]].drop_duplicates().sort_values(by=["City", "Address Without Number"], ignore_index=True)
df_shop_info.to_sql(name="shop_info", con=engine, if_exists="replace")

# Create SQL table for the charts on sentiment.
df_pie_chart_sentiment = df_enriched.groupby(["City", "Address Without Number", "Month", "Group Name", "Sentiment"])["Sentiment"].count().reset_index(name="Count")
df_pie_chart_sentiment.to_sql(name="sentiment", con=engine, if_exists="replace")

# Create SQL table for the KPIs and the map: number of comments, number of ratings, average rating, latitude and longitude of the cities.
groupby_filter = df_enriched.groupby(["City", "Address Without Number", "Month", "Is Open", "Latitude", "Longitude"])
df_nb_comments = groupby_filter["Content"].count().reset_index(name="Number of Comments")
df_nb_ratings = groupby_filter["Rating"].count().reset_index(name="Number of Ratings")
df_rating = groupby_filter["Rating"].mean().round(2).reset_index(name="Average Rating")
df_metrics_map = pd.concat([df_nb_comments, df_nb_ratings[["Number of Ratings"]], df_rating[["Average Rating"]]], axis=1)
# lower_tertile_point = df_map["Average Rating"].quantile(0.33)
# upper_tertile_point = df_map["Average Rating"].quantile(0.66)
# df_map["Rating Tertile"] = df_map["Average Rating"].apply(lambda x: f"Moins de {lower_tertile_point}" if x < lower_tertile_point else (f"Plus de {upper_tertile_point}" if x > upper_tertile_point else f"Entre {lower_tertile_point} et {upper_tertile_point}"))
df_metrics_map.to_sql(name="metrics_map", con=engine, if_exists="replace")

# Create SQL table for NMF results.
df_nmf_bad = load_nlp_data(file_setting.get("NMF_BAD_DATA"))
df_nmf_good = load_nlp_data(file_setting.get("NMF_GOOD_DATA"))
df_nmf_bad.to_sql(name="nmf_bad", con=engine, if_exists="replace")
df_nmf_good.to_sql(name="nmf_good", con=engine, if_exists="replace")

# Create SQL table for wordcloud.
df_wordcloud = load_nlp_data(file_setting.get("WORDCLOUD_DATA"))
df_wordcloud.to_sql(name="wordcloud", con=engine, if_exists="replace")

# Create SQL table for the table of raw comments.
df_raw_comments = df_enriched[["City", "Address Without Number", "Date", "Content", "Sentiment", "Rating"]].dropna(subset=["Content"]).drop_duplicates().sort_values(by=["City", "Address Without Number", "Date"], ignore_index=True)
df_raw_comments.to_sql(name="raw_comments", con=engine, if_exists="replace")
