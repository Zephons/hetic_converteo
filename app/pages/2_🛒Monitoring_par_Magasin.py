import os
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from sqlalchemy import create_engine


postgresql_uri = os.environ["DATABASE_URL"]
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
}
</style>
"""
, unsafe_allow_html=True)

# Sélectionner une ville.
sql_city = """
    SELECT DISTINCT "City" FROM public.city_address_date;
"""
df_city = pd.read_sql_query(sql_city, engine)
index_paris = int(df_city.index[df_city["City"] == "Paris"][0])
selected_city = st.sidebar.selectbox("Ville :", df_city["City"], index_paris)

# Sélectionner une adresse.
sql_address = f"""
    SELECT DISTINCT "Address Without Number" FROM public.city_address_date WHERE "City" = $${selected_city}$$;
"""
df_address = pd.read_sql_query(sql_address, engine)
selected_address = st.sidebar.selectbox("Adresse :", df_address["Address Without Number"])

# Sélectionner les dates de début et de fin.
sql_dates = f"""
    SELECT MIN("Date") AS "Min Date", MAX("Date") AS "Max Date" FROM public.city_address_date WHERE "City" = $${selected_city}$$ AND "Address Without Number" = $${selected_address}$$;
"""
df_dates = pd.read_sql_query(sql_dates, engine)
min_date, max_date = df_dates.values[0]
default_date = min(date(2022, 1, 1), max_date)
selected_min_date = st.sidebar.date_input("Date de début :", value=default_date, min_value=min_date, max_value=max_date)
selected_max_date = st.sidebar.date_input("Date de fin :", value=max_date, min_value=selected_min_date, max_value=max_date)

# Metric nombre d'avis.
sql_metrics = f"""
    SELECT SUM("Number of Comments")::TEXT AS "Sum Comments", SUM("Number of Ratings")::TEXT AS "Sum Ratings", ROUND(AVG("Average Rating")::NUMERIC, 2) AS "Aggregated Average Rating" FROM public.metrics WHERE "City" = $${selected_city}$$ AND "Address Without Number" = $${selected_address}$$ AND "Date" >= '{selected_min_date}' AND "Date" <= '{selected_max_date}';
"""
df_metrics = pd.read_sql_query(sql_metrics, engine)
sum_comments, sum_ratings, aggregated_average_rating = df_metrics.values[0]
metric_col1, metric_col2, metric_col3 = st.columns(3)
metric_col1.metric("Nombre d'avis", sum_comments)
metric_col2.metric("Nombre de notes", sum_ratings)
metric_col3.metric("Note moyenne", f"{aggregated_average_rating} / 5")

# Pie chart Sentiment.
sql_pie_chart_sentiment = f"""
    SELECT "Sentiment", SUM("Count") AS "Sum" FROM public.pie_chart_sentiment WHERE "City" = $${selected_city}$$ AND "Address Without Number" = $${selected_address}$$ AND "Date" >= '{selected_min_date}' AND "Date" <= '{selected_max_date}' GROUP BY "Sentiment";
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

st.sidebar.title("À propos")
st.sidebar.info(
"""
    Code source : [github.com/Zephons/hetic_converteo](https://github.com/Zephons/hetic_converteo)
"""
)