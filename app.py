import streamlit as st
import pandas as pd

st.title('test')

df = pd.DataFrame()
data = st.data_editor(df)

