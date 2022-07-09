import os
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine


st.set_page_config(page_title="Dashboard Castorama", page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)

postgresql_uri = os.environ["DATABASE_URL"]
engine = create_engine(postgresql_uri.replace("postgres", "postgresql"))

# Selectionner une ville
sql_city = """
    SELECT DISTINCT "City" FROM public.pie_chart;
"""
df_city = pd.read_sql_query(sql_city, engine)
selected_city = st.sidebar.selectbox("Ville :", df_city["City"])

# Selectionner une adresse
sql_address = f"""
    SELECT DISTINCT "Address Without Number" FROM public.pie_chart WHERE "City" = $${selected_city}$$;
"""
df_address = pd.read_sql_query(sql_address, engine)
selected_address = st.sidebar.selectbox("Adresse :", df_address["Address Without Number"])

# Pie chart Sentiment
sql_pie_chart = f"""
    SELECT "Sentiment", sum("Count") FROM public.pie_chart WHERE "City" = $${selected_city}$$ AND "Address Without Number" = $${selected_address}$$ group by "Sentiment";
"""
df_pie_chart = pd.read_sql_query(sql_pie_chart, engine)
fig = px.pie(names=df_pie_chart["Sentiment"], values=df_pie_chart["sum"])
st.plotly_chart(fig)