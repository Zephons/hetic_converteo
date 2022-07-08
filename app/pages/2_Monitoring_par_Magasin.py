import os
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine


st.set_page_config(page_title="Dashboard Castorama", page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)

postgresql_uri = os.environ["DATABASE_URL"]
engine = create_engine(postgresql_uri.replace("postgres", "postgresql"))

# Selectionner un magasin
sql_business_id = """
    SELECT DISTINCT "Business Id" FROM public.pie_chart;
"""
df_business_id = pd.read_sql_query(sql_business_id, engine)
selected_business_id = st.sidebar.selectbox('Selectionner un magasin: ', df_business_id["Business Id"])

# Pie chart
sql_pie_chart = f"""
    SELECT "Sentiment", sum("Count") FROM public.pie_chart WHERE "Business Id" = '{selected_business_id}' group by "Sentiment";
"""
df_pie_chart = pd.read_sql_query(sql_pie_chart, engine)
fig = px.pie(names=df_pie_chart["Sentiment"], values=df_pie_chart["sum"])
st.plotly_chart(fig)