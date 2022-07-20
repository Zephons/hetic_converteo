import streamlit as st


def set_markdown():
    st.set_page_config(page_title="Dashboard Castorama", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
    st.markdown("""
    <style>
    div[data-testid="metric-container"] {
    background-color: rgba(28, 131, 225, 0.1);
    border: 1px solid rgba(28, 131, 225, 0.1);
    padding: 2% 2% 2% 10%;
    border-radius: 5px;
    color: rgb(30, 103, 119);
    overflow-wrap: break-word;
    font-size: 10px;
    }
    </style>
    """
    , unsafe_allow_html=True)

def set_about():
    st.sidebar.title("À propos")
    st.sidebar.info("""
        Code source : [github.com/Zephons/hetic_converteo](https://github.com/Zephons/hetic_converteo)
    """
    )