import streamlit as st
import pandas as pd
import well_profile as wp
from io import StringIO
from math import degrees, radians, cos, sin, acos

import plotly.express as px
import plotly.graph_objects as go

def prep_data(string):
    values = string.split()
    grouped_values = [values[i:i + 3] for i in range(0, len(values), 3)]
    df = pd.DataFrame(grouped_values, columns=['md', 'inc', 'azi'])
    df[['md', 'inc', 'azi']] = df[['md', 'inc', 'azi']].apply(pd.to_numeric)
    df.dropna(axis=1, how='all', inplace=True)
    df.dropna(inplace=True)
    return df

def load_data(data):
    trajectory = [{'md': 0, 'inc': 0, 'azi': 0, 'dl': 0, 'tvd': 0, 'north': 0, 'east': 0}]

    for idx, row in data.iterrows():
        if row['md'] > 0:
            dogleg = calc_dogleg(trajectory[-1]['inc'], row['inc'], trajectory[-1]['azi'], row['azi'])
            new_point = {
                'md': row['md'], 
                'inc': row['inc'], 
                'azi': row['azi'],
                'north': calc_north(trajectory[-1]['north'], trajectory[-1]['md'], row['md'], trajectory[-1]['inc'], row['inc'], trajectory[-1]['azi'], row['azi'], dogleg),
                'east': calc_east(trajectory[-1]['east'], trajectory[-1]['md'], row['md'], trajectory[-1]['inc'], row['inc'], trajectory[-1]['azi'], row['azi'], dogleg),
                'tvd': calc_tvd(trajectory[-1]['tvd'], trajectory[-1]['md'], row['md'], trajectory[-1]['inc'], row['inc'], dogleg),
                'dl': degrees(dogleg)
            }
            trajectory.append(new_point)

    return pd.DataFrame(trajectory[1:])  # Skip the initial dummy point

def calc_dogleg(inc1, inc2, azi1, azi2):
    if inc1 == inc2 and azi1 == azi2:
        dl = 0
    else:
        inner_value = cos(radians(inc1)) * cos(radians(inc2)) + sin(radians(inc1)) * sin(radians(inc2)) * \
            cos(radians(azi2 - azi1))
        if inner_value > 1:
            inner_value = 1
        if inner_value < -1:
            inner_value = -1
        dl = acos(inner_value)
    return dl


st.title('test4')

raw_data = st.text_area('data')

if raw_data:
    df = prep_data(raw_data)
    df = load_data(df)
    st.write(df)