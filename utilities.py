import pandas as pd
from io import StringIO

import plotly.express as px
import plotly.graph_objects as go

def create_df(string):
    values = string.split()
    grouped_values = [values[i:i + 3] for i in range(0, len(values), 3)]
    df = pd.DataFrame(grouped_values, columns=['md', 'inc', 'azi'])
    return df

def process_df(df):
    df.dropna(axis=1, how='all', inplace=True)
    df.dropna(inplace=True)
    return df

