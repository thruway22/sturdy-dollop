import streamlit as st
import pandas as pd

st.title('test')

df = pd.DataFrame(columns=['md', 'inc', 'azi'])
data = st.data_editor(df)

