import os
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine


st.set_page_config(page_title="Dashboard Castorama", page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)

postgresql_uri = os.environ["DATABASE_URL"]
engine = create_engine(postgresql_uri.replace("postgres", "postgresql"))

# Sélectionner les dates de début et de fin
sql_dates = f"""
    SELECT MIN("Date") AS "Min Date", MAX("Date") AS "Max Date" FROM public.city_address_date;
"""
df_dates = pd.read_sql_query(sql_dates, engine)
min_date, max_date = df_dates.values[0]
selected_min_date = st.sidebar.date_input("Date de début :", value=min_date, min_value=min_date, max_value=max_date)
selected_max_date = st.sidebar.date_input("Date de fin :", value=max_date, min_value=selected_min_date, max_value=max_date)

# Pie chart Sentiment
sql_pie_chart = f"""
    SELECT "Sentiment", SUM("Count") AS "Sum" FROM public.pie_chart_sentiment WHERE "Date" >= '{selected_min_date}' AND "Date" <= '{selected_max_date}' GROUP BY "Sentiment";
"""
df_pie_chart = pd.read_sql_query(sql_pie_chart, engine)
fig = px.pie(names=df_pie_chart["Sentiment"], values=df_pie_chart["Sum"])
st.plotly_chart(fig)