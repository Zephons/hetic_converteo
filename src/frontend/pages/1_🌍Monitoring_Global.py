import os
import sys
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

from src.backend.methods import get_file_setting, get_secrets
from src.frontend.charts.charts_global import get_metrics_global, get_pie_chart_sentiment_global, get_bar_chart_group_global, get_map_global, get_bar_chart_good_topics_global, get_bar_chart_bad_topics_global
from src.frontend.charts.widgets_in_common import set_markdown_global, set_about


file_setting = get_file_setting("settings.yml")
secrets = get_secrets(file_setting.get("SECRETS"))
postgresql_uri = os.environ.get("DATABASE_URL") or secrets.get("POSTGRESQL").get("URI")
mapbox_token = os.environ.get("MAPBOX_TOKEN") or secrets.get("MAPBOX").get("ACCESS_TOKEN")
engine = create_engine(postgresql_uri.replace("postgres", "postgresql"))

set_markdown_global()

st.sidebar.image(file_setting.get("CASTO_LOGO_1"))

# Select a start date and an end date.
sql_dates = f"""
    SELECT MIN("Month") AS "Min date", MAX("Month") AS "Max Date" FROM public.filters;
"""
df_dates = pd.read_sql_query(sql_dates, engine)
min_date, max_date = df_dates.values[0]
selected_min_date, selected_max_date = st.sidebar.slider("📅 Période :", value=(min_date, max_date), min_value=min_date, max_value=max_date, format="MM/Y")
st.sidebar.markdown(f"Période sélectionnée : {selected_min_date.strftime('%m / %Y')} - {selected_max_date.strftime('%m / %Y')}")

set_about()

# Shop info and KPIs (number of comments, number of ratings, average rating).
st.title("KPIs")
nb_shops_in_operation, nb_shops, sum_comments, sum_ratings, sum_comments_per_shop, aggregated_average_rating = get_metrics_global(engine, selected_min_date, selected_max_date)
metric_row1_col1, metric_row1_col2, metric_row1_col3, metric_row1_col4, metric_row1_col5 = st.columns((1, 1, 1, 1, 1))
metric_row1_col1.metric("Magasins en activité", f"{nb_shops_in_operation} / {nb_shops}")
metric_row1_col2.metric("Nombre d'avis", sum_comments)
metric_row1_col3.metric("Nombre moyen d'avis", sum_comments_per_shop)
metric_row1_col4.metric("Nombre de notes", sum_ratings)
metric_row1_col5.metric("Note moyenne", f"{aggregated_average_rating} / 5")

# Disable Plotly toolbar
plotly_config = {'displayModeBar': False}

# Geographical Map with regards to rating.
st.title("Répartition géographique de la performance des magasins par ville")
st.caption("La taille des bulles correspond au nombre des notes et la couleur correspond à la note moyennne.")
map_global = get_map_global(engine, secrets, selected_min_date, selected_max_date)
st.plotly_chart(map_global, config=plotly_config, use_container_width=True)

metric_row2_col1, metric_row2_col2 = st.columns((1, 1))
# Pie chart Sentiment.
metric_row2_col1.title("Répartition des sentiments")
pie_chart_sentiment_global = get_pie_chart_sentiment_global(engine, selected_min_date, selected_max_date)
metric_row2_col1.plotly_chart(pie_chart_sentiment_global, config=plotly_config, use_container_width=True)
# Bar chart Group.
metric_row2_col2.title("Répartition des sentiments par région")
bar_chart_group_global = get_bar_chart_group_global(engine, selected_min_date, selected_max_date)
metric_row2_col2.plotly_chart(bar_chart_group_global, config=plotly_config, use_container_width=True)

metric_row3_col1, metric_row3_col2= st.columns((1, 1))
# Bar chart NMF good topics.
metric_row3_col1.title("Nombre d'avis positifs par thématique client.")
bar_chart_good_topics_par_magasin = get_bar_chart_good_topics_global(engine, selected_min_date, selected_max_date)
metric_row3_col1.plotly_chart(bar_chart_good_topics_par_magasin, config=plotly_config, use_container_width=True)
# Bar chart NMF bad topics.
metric_row3_col2.title("Nombre d'avis négatifs par thématique client.")
bar_chart_bad_topics_par_magasin = get_bar_chart_bad_topics_global(engine, selected_min_date, selected_max_date)
metric_row3_col2.plotly_chart(bar_chart_bad_topics_par_magasin, config=plotly_config, use_container_width=True)
