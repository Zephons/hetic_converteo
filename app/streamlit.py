import streamlit as st
import time
import numpy as np
import pandas as pd

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()

last_rows = np.random.randn(1, 1)
chart = st.line_chart(last_rows)

for i in range(1, 16):
    new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    status_text.text(f'{i}% Completed.')
    progress_bar.progress(i)
    chart.add_rows(new_rows)

    time.sleep(0.1)

progress_bar.empty()

st.button('Re-run')

st.header('Group 9')

df_casto = pd.read_excel("data/sample.xlsx", header=[1])
st.dataframe(df_casto)