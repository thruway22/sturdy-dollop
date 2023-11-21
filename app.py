import streamlit as st
import pandas as pd

st.title('test')

# df = pd.DataFrame([[0, 0, 0]], columns=["md", "inc", "azi"])
# data = st.data_editor(df)

data = st.text_area('data')

