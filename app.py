import streamlit as st
import pandas as pd
from io import StringIO
import well_profile as wp

st.title('test')

# df = pd.DataFrame([[0, 0, 0]], columns=["md", "inc", "azi"])
# data = st.data_editor(df)

data = st.text_area('data')

def convert_to_csv(input_string):
    values = input_string.split()
    # Group every three values
    grouped_values = [values[i:i + 3] for i in range(0, len(values), 3)]
    df = pd.DataFrame(grouped_values, columns=['a', 'b', 'c'])
    return df

st.write(convert_to_csv(data))

wp = wp.load(df)


# wp.plot(style={'color': 'dls', 'size': 5}).show()
