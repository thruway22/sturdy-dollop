import streamlit as st
import pandas as pd
from io import StringIO
import well_profile as wp
import plotly.express as px
import plotly.graph_objects as go

st.title('test')

# df = pd.DataFrame([[0, 0, 0]], columns=["md", "inc", "azi"])
# data = st.data_editor(df)

data = st.text_area('data')


def plot(well):
    units = well.info['units']

    well1 = pd.DataFrame(well.trajectory)
    well1["well"] = 1
    result = well1

    color = 'well'
    fig = px.line_3d(result, x="east", y="north", z="tvd", color=color)

def convert_to_csv(input_string):
    values = input_string.split()
    # Group every three values
    grouped_values = [values[i:i + 3] for i in range(0, len(values), 3)]
    df = pd.DataFrame(grouped_values, columns=['md', 'inc', 'azi'])
    return df

df = convert_to_csv(data)
st.write(df)

wp = wp.load(df)
st.plotly_chart(wp.load(df).plot())

# wp.plot(style={'color': 'dls', 'size': 5}).show()
