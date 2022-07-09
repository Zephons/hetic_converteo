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

# # Table pour line chart Rating



# Table pour pie chart Sentiment
df_pie = df_enriched.groupby(["City", "Address Without Number", "Sentiment"])["Sentiment"].count().reset_index(name="Count")
df_pie.to_sql(name="pie_chart", con=engine, if_exists="replace")

