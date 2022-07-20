import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from sqlalchemy import create_engine
sys.path.append(os.getcwd())

from src.backend.methods import get_file_setting, get_secrets


file_setting = get_file_setting("settings.yml")
secrets = get_secrets(file_setting.get("SECRETS"))
postgresql_uri = os.environ.get("DATABASE_URL") or secrets.get("POSTGRESQL").get("URI")
mapbox_token = os.environ.get("MAPBOX_TOKEN") or secrets.get("MAPBOX").get("ACCESS_TOKEN")
engine = create_engine(postgresql_uri.replace("postgres", "postgresql"))

st.set_page_config(page_title="Dashboard Castorama", page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)
st.markdown("""
<style>
div[data-testid="metric-container"] {
   background-color: rgba(28, 131, 225, 0.1);
   border: 1px solid rgba(28, 131, 225, 0.1);
   padding: 5% 5% 5% 10%;
   border-radius: 5px;
   color: rgb(30, 103, 119);
   overflow-wrap: break-word;
   font-size: 10px;
}
</style>
"""
, unsafe_allow_html=True)

# Sélectionner les dates de début et de fin
sql_dates = f"""
    SELECT MIN("Date") AS "Min Date", MAX("Date") AS "Max Date" FROM public.city_address_date;
"""
df_dates = pd.read_sql_query(sql_dates, engine)
min_date, max_date = df_dates.values[0]
default_date = min(date(2022, 1, 1), max_date)
selected_min_date = st.sidebar.date_input("📅 Date de début :", value=default_date, min_value=min_date, max_value=max_date)
selected_max_date = st.sidebar.date_input("📅 Date de fin :", value=max_date, min_value=selected_min_date, max_value=max_date)

st.sidebar.title("À propos")
st.sidebar.info("""
    Code source : [github.com/Zephons/hetic_converteo](https://github.com/Zephons/hetic_converteo)
"""
)

# Metric nombre d'avis.
sql_metrics = f"""
    SELECT SUM("Number of Comments")::TEXT AS "Sum Comments", SUM("Number of Ratings")::TEXT AS "Sum Ratings", ROUND(AVG("Average Rating")::NUMERIC, 2) AS "Aggregated Average Rating" FROM public.metrics WHERE "Date" >= '{selected_min_date}' AND "Date" <= '{selected_max_date}';
"""
df_metrics = pd.read_sql_query(sql_metrics, engine)
sum_comments, sum_ratings, aggregated_average_rating = df_metrics.values[0]
metric_col1, metric_col2, metric_col3 = st.columns(3)
metric_col1.metric("Nombre d'avis", sum_comments)
metric_col2.metric("Nombre de notes", sum_ratings)
metric_col3.metric("Note moyenne", f"{aggregated_average_rating} / 5")

# Pie chart Sentiment
sql_pie_chart_sentiment = f"""
    SELECT "Sentiment", SUM("Count") AS "Sum" FROM public.pie_chart_sentiment WHERE "Date" >= '{selected_min_date}' AND "Date" <= '{selected_max_date}' GROUP BY "Sentiment";
"""
df_pie_chart_sentiment = pd.read_sql_query(sql_pie_chart_sentiment, engine)
fig_pie_chart_sentiment = px.pie(
    names=df_pie_chart_sentiment["Sentiment"],
    values=df_pie_chart_sentiment["Sum"],
    title='Sentiment des avis',
    color=df_pie_chart_sentiment["Sentiment"],
    color_discrete_map={
        "Négatif": "#EF553B",
        "Positif": "#00CC96",
        "Neutre": "#636EFA"})
fig_pie_chart_sentiment.update_traces(textinfo="percent+label")
fig_pie_chart_sentiment.update_layout(
    autosize=False,
    width=500,
    height=500,
    font={"size": 15},
    title_x=0.5,
    showlegend=False)
st.plotly_chart(fig_pie_chart_sentiment)

# Carte géographique de Rating.
sql_map_rating = f"""
    SELECT "Zipcode", "Departement", "average_rating_departement" FROM public.map_rating WHERE "Creation date" >= '{selected_min_date}' AND "Creation date" <= '{selected_max_date}';
"""
new_df_google = pd.read_sql_query(sql_map_rating, engine)