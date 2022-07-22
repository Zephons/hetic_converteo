import os
import sys
import pandas as pd
import streamlit as st
from datetime import date
from sqlalchemy import create_engine
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

from src.backend.methods import get_file_setting, get_secrets
from src.frontend.charts.charts_par_magasin import get_metrics_par_magasin, get_pie_chart_sentiment_par_magasin
from src.frontend.charts.widgets_in_common import set_markdown, set_about


file_setting = get_file_setting("settings.yml")
secrets = get_secrets(file_setting.get("SECRETS"))
postgresql_uri = os.environ.get("DATABASE_URL") or secrets.get("POSTGRESQL").get("URI")
engine = create_engine(postgresql_uri.replace("postgres", "postgresql"))

set_markdown()

# Sélectionner une ville.
sql_city = """
    SELECT DISTINCT "City" FROM public.filters;
"""
df_city = pd.read_sql_query(sql_city, engine)
index_paris = int(df_city.index[df_city["City"] == "Paris"][0])
selected_city = st.sidebar.selectbox("🏙️ Ville :", df_city["City"], index_paris)

# Sélectionner une adresse.
sql_address = f"""
    SELECT DISTINCT "Address Without Number" FROM public.filters WHERE "City" = $${selected_city}$$;
"""
df_address = pd.read_sql_query(sql_address, engine)
selected_address = st.sidebar.selectbox("📍 Adresse :", df_address["Address Without Number"])

# Sélectionner les dates de début et de fin.
sql_dates = f"""
    SELECT MIN("Date") AS "Min Date", MAX("Date") AS "Max Date" FROM public.filters WHERE "City" = $${selected_city}$$ AND "Address Without Number" = $${selected_address}$$;
"""
df_dates = pd.read_sql_query(sql_dates, engine)
min_date, max_date = df_dates.values[0]
default_date = min(date(2022, 1, 1), max_date)
selected_min_date = st.sidebar.date_input("📅 Date de début :", value=default_date, min_value=min_date, max_value=max_date)
selected_max_date = st.sidebar.date_input("📅 Date de fin :", value=max_date, min_value=selected_min_date, max_value=max_date)

set_about()

selected_chart_type = st.selectbox("Type de graphique :", ["KPIs", "Traitement automatique du langage naturel"])
if selected_chart_type == "KPIs":
    # Métriques sur nombre d'avis, nombre de rating, rating moyen.
    group_name, is_open, sum_comments, sum_ratings, aggregated_average_rating = get_metrics_par_magasin(engine, selected_city, selected_address, selected_min_date, selected_max_date)
    status = "En activité" if is_open else "Fermé"
    average_rating = f"{aggregated_average_rating} / 5" if aggregated_average_rating else "—"
    metric_col1, metric_col2, metric_col3, metric_col4, metric_col5 = st.columns(5)
    metric_col1.metric("Statut", status)
    metric_col2.metric("Groupe", group_name)
    metric_col3.metric("Nombre d'avis", sum_comments)
    metric_col4.metric("Nombre de notes", sum_ratings)
    metric_col5.metric("Note moyenne", average_rating)

    # Pie chart Sentiment.
    pie_chart_sentiment_par_magasin = get_pie_chart_sentiment_par_magasin(engine, selected_city, selected_address, selected_min_date, selected_max_date)
    st.plotly_chart(pie_chart_sentiment_par_magasin)