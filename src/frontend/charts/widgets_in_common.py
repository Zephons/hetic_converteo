import streamlit as st

def set_markdown_home():
    st.set_page_config(page_title="Dashboard Castorama", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
    st.markdown("""
    <style>

    </style>
    """
    , unsafe_allow_html=True)

def set_markdown_global():
    st.set_page_config(page_title="Dashboard Castorama", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
    st.markdown("""
    <style>
    div[data-testid="metric-container"] {
        background-color: rgba(28, 131, 225, 0.1);
        border: 1px solid rgba(28, 131, 225, 0.1);
        padding: 2% 2% 2% 5%;
        border-radius: 5px;
        color: rgb(30, 103, 119);
        overflow-wrap: break-word;
    }
    div[class="StyledThumbValue css-jsz2xw e88czh82"] {
        color: transparent;
    }
    span[class="css-10trblm e16nr0p30"] {
        font-size: 23px;
    }
    div[data-testid="stCaptionContainer"] {
        font-size: 16px;
    }
    div[data-testid="stMetricValue"] > div {
        font-size: 23px;
    }
    </style>
    """
    , unsafe_allow_html=True)

def set_markdown_par_magasin():
    st.set_page_config(page_title="Dashboard Castorama", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
    st.markdown("""
    <style>
    div[data-testid="metric-container"] {
    background-color: rgba(28, 131, 225, 0.1);
    border: 1px solid rgba(28, 131, 225, 0.1);
    padding: 2% 2% 2% 5%;
    border-radius: 5px;
    color: rgb(30, 103, 119);
    overflow-wrap: break-word;
    }
    div[class="StyledThumbValue css-jsz2xw e88czh82"] {
        color: transparent;
    }
    span[class="css-10trblm e16nr0p30"] {
        font-size: 23px;
    }
    div[data-testid="stCaptionContainer"] {
        font-size: 16px;
    }
    div[data-testid="stMetricValue"] > div {
        font-size: 23px;
    }
    </style>
    """
    , unsafe_allow_html=True)

def set_about():
    st.sidebar.title("À propos")
    st.sidebar.info("""
        Cette application est un outil de veille construit par un groupe d'étudiants de l'HETIC pour le cabinet de conseil Converteo. L'objectif de cet outil est de suivre les insights consommateurs sur Castorama, distributeur français d'outils et de fournitures de bricolage.
    """
    )