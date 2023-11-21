import pandas as pd
from io import StringIO

import plotly.express as px
import plotly.graph_objects as go

def prep_data(string):
    values = string.split()
    grouped_values = [values[i:i + 3] for i in range(0, len(values), 3)]
    df = pd.DataFrame(grouped_values, columns=['md', 'inc', 'azi'])
    df.dropna(axis=1, how='all', inplace=True)
    df.dropna(inplace=True)
    return df

def load_data(data, set_start=None):
    trajectory = [{'md': 0, 'inc': 0, 'azi': 0, 'dl': 0, 'tvd': 0, 'north': initial_point['north'], 'east': initial_point['east']}]

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
