import os
import sys
import pandas as pd
import streamlit as st
from datetime import date
from sqlalchemy import create_engine
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

from src.backend.methods import get_file_setting, get_secrets
from src.frontend.charts.charts_global import get_metrics_global, get_pie_chart_sentiment_global, get_map_global
from src.frontend.charts.widgets_in_common import set_markdown, set_about


file_setting = get_file_setting("settings.yml")
secrets = get_secrets(file_setting.get("SECRETS"))
postgresql_uri = os.environ.get("DATABASE_URL") or secrets.get("POSTGRESQL").get("URI")
mapbox_token = os.environ.get("MAPBOX_TOKEN") or secrets.get("MAPBOX").get("ACCESS_TOKEN")
engine = create_engine(postgresql_uri.replace("postgres", "postgresql"))

set_markdown()

# Sélectionner les dates de début et de fin.
sql_dates = f"""
    SELECT MIN("Date") AS "Min Date", MAX("Date") AS "Max Date" FROM public.filters;
"""
df_dates = pd.read_sql_query(sql_dates, engine)
min_date, max_date = df_dates.values[0]
default_date = min(date(2022, 1, 1), max_date)
selected_min_date = st.sidebar.date_input("📅 Date de début :", value=default_date, min_value=min_date, max_value=max_date)
selected_max_date = st.sidebar.date_input("📅 Date de fin :", value=max_date, min_value=selected_min_date, max_value=max_date)

set_about()

selected_chart_type = st.selectbox("Type de graphique :", ["KPIs", "Carte géographique"])
if selected_chart_type == "KPIs":
    # Métriques sur nombre d'avis, nombre de rating, rating moyen.
    sum_comments, sum_ratings, aggregated_average_rating = get_metrics_global(engine, selected_min_date, selected_max_date)
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("Nombre d'avis", sum_comments)
    metric_col2.metric("Nombre de notes", sum_ratings)
    metric_col3.metric("Note moyenne", f"{aggregated_average_rating} / 5")

    # Pie chart Sentiment.
    pie_chart_sentiment_global = get_pie_chart_sentiment_global(engine, selected_min_date, selected_max_date)
    st.plotly_chart(pie_chart_sentiment_global)
else:
    # Carte géographique de Rating.
    map_global = get_map_global(engine, selected_min_date, selected_max_date)
    st.plotly_chart(map_global)