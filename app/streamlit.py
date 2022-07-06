import streamlit as st
import time
import numpy as np
import pandas as pd

st.set_page_config(page_title='Dashboard Casto', page_icon=None, layout='centered', initial_sidebar_state='auto', menu_items=None)

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()

last_rows = np.random.randn(1, 1)
chart = st.line_chart(last_rows)

for i in range(1, 101):
    new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    status_text.text(f'{i}% Completed.')
    progress_bar.progress(i)
    chart.add_rows(new_rows)

progress_bar.empty()

st.button('Re-run')

st.header('Group 9')
df_casto = pd.read_excel("data/sample.xlsx", header=[1])
st.dataframe(df_casto)
df_casto_google = df_casto[df_casto['Platform'] == 'GOOGLE_MY_BUSINESS']

import plotly.express as px
# On rajoute une colonne rating moyen par ville.
Avg_city_rating = df_casto_google[['City','Rating']]
Avg_city_rating = Avg_city_rating.groupby('City', as_index=False)['Rating'].mean()
Avg_city_rating['Rating'] = Avg_city_rating['Rating'].round(2)

# On retrouve les departements à partir des adresses.
df_departements = pd.read_csv('data/departements-france.csv')
df_departements['code_departement'] = df_departements['code_departement'].astype('str')
df_departements['code_departement'] = df_departements['code_departement'].apply(lambda x: x if len(x) > 1 else '0'+x)
Region_dict = dict(zip(df_departements['code_departement'],df_departements['nom_region']))
Depart_dict = dict(zip(df_departements['code_departement'],df_departements['nom_departement']))
avg_rating_dict = dict(zip(Avg_city_rating['City'],Avg_city_rating['Rating']))
df_casto_google['Region'] = df_casto_google['Zipcode'].map(Region_dict)
df_casto_google['Departement'] = df_casto_google['Zipcode'].map(Depart_dict)
df_casto_google['average_rating'] = df_casto_google['City'].map(avg_rating_dict)
fig = px.scatter(df_casto_google, x="average_rating", y="City",
         size="average_rating", color="City",
                 hover_name="City", log_x=True, size_max=15)
st.plotly_chart(fig)