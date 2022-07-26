import os
import sys
import streamlit as st
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

from src.backend.methods import get_file_setting
from src.frontend.charts.widgets_in_common import set_markdown_home, set_about

file_setting = get_file_setting("settings.yml")

set_markdown_home()

st.sidebar.image(file_setting.get("CASTO_LOGO_1"))

st.header("Architecture de l'application")

set_about()