import streamlit as st


st.set_page_config(page_title="Dashboard Castorama", page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)

st.header("Architecture de l'application")

st.sidebar.title("À propos")
st.sidebar.info(
"""
    Code source : [github.com/Zephons/hetic_converteo](https://github.com/Zephons/hetic_converteo)
"""
)