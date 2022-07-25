import os
import sys
import streamlit as st
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

from src.frontend.charts.widgets_in_common import set_markdown_home, set_about


set_markdown_home()

st.sidebar.image("src/images/Castorama-logo.png")

st.header("Architecture de l'application")

set_about()