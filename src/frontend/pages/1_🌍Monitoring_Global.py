import os
import sys
import pandas as pd
import streamlit as st
from datetime import date
from sqlalchemy import create_engine
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

from src.backend.methods import get_file_setting, get_secrets
from src.frontend.charts.charts_global import get_metrics_global, get_pie_chart_sentiment_global, get_bar_chart_group_global, get_line_chart_rating_global, get_map_global
from src.frontend.charts.widgets_in_common import set_markdown_global, set_about


file_setting = get_file_setting("settings.yml")
secrets = get_secrets(file_setting.get("SECRETS"))
postgresql_uri = os.environ.get("DATABASE_URL") or secrets.get("POSTGRESQL").get("URI")
mapbox_token = os.environ.get("MAPBOX_TOKEN") or secrets.get("MAPBOX").get("ACCESS_TOKEN")
engine = create_engine(postgresql_uri.replace("postgres", "postgresql"))

set_markdown_global()

# Select a start date and an end date.
sql_dates = f"""
    SELECT MIN("Date") AS "Min Date", MAX("Date") AS "Max Date" FROM public.filters;
"""
df_dates = pd.read_sql_query(sql_dates, engine)
min_date, max_date = df_dates.values[0]
default_date = min(date(2022, 1, 1), max_date)
selected_min_date = st.sidebar.date_input("📅 Date de début :", value=default_date, min_value=min_date, max_value=max_date)
selected_max_date = st.sidebar.date_input("📅 Date de fin :", value=max_date, min_value=selected_min_date, max_value=max_date)

set_about()

# Shop info and KPIs (number of comments, number of ratings, average rating).
nb_shops_in_operation, nb_shops, sum_comments, sum_ratings, sum_comments_per_shop, aggregated_average_rating = get_metrics_global(engine, selected_min_date, selected_max_date)
metric_row1_col1, metric_row1_col2, metric_row1_col3, metric_row1_col4, metric_row1_col5 = st.columns(5)
metric_row1_col1.metric("Nombre de magasins en activité", f"{nb_shops_in_operation} / {nb_shops}")
metric_row1_col2.metric("Nombre d'avis", sum_comments)
metric_row1_col3.metric("Nombre de notes", sum_ratings)
metric_row1_col4.metric("Nombre d'avis par magasin", sum_comments_per_shop)
metric_row1_col5.metric("Note moyenne", f"{aggregated_average_rating} / 5")

metric_row2_col1, metric_row2_col2 = st.columns(2)
# Pie chart Sentiment.
pie_chart_sentiment_global = get_pie_chart_sentiment_global(engine, selected_min_date, selected_max_date)
metric_row2_col1.plotly_chart(pie_chart_sentiment_global)

metric_row3_col1, metric_row3_col2 = st.columns(2)
# Bar chart Group.
bar_chart_group_global = get_bar_chart_group_global(engine, selected_min_date, selected_max_date)
metric_row3_col1.plotly_chart(bar_chart_group_global)
# Line chart Rating.
line_chart_rating_global = get_line_chart_rating_global(engine, selected_min_date, selected_max_date)
metric_row3_col2.plotly_chart(line_chart_rating_global)

# Geographical Map with regards to rating.
map_global = get_map_global(engine, selected_min_date, selected_max_date)
st.plotly_chart(map_global)