import streamlit as st
import pandas as pd
from math import degrees, radians, cos, sin, acos, tan
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='DLS Plotter')
st.write(15)

def prep_data(string):
    values = string.split()
    grouped_values = [values[i:i + 3] for i in range(0, len(values), 3)]
    df = pd.DataFrame(grouped_values, columns=['md', 'inc', 'azi'])
    df[['md', 'inc', 'azi']] = df[['md', 'inc', 'azi']].apply(pd.to_numeric, errors='coerce')
    df.dropna(axis=1, how='all', inplace=True)
    df.dropna(inplace=True)
    return df

def load_data(data):
    trajectory = [{'md': 0, 'inc': 0, 'azi': 0, 'dls': 0, 'tvd': 0, 'north': 0, 'east': 0}]
    for idx, row in data.iterrows():
        if row['md'] > 0:
            beta = compute_beta(trajectory[-1]['inc'], row['inc'], trajectory[-1]['azi'], row['azi'])
            new_point = {
                'md': row['md'], 
                'inc': row['inc'], 
                'azi': row['azi'],
                'north': compute_north(trajectory[-1]['north'], trajectory[-1]['md'], row['md'], trajectory[-1]['inc'], row['inc'], trajectory[-1]['azi'], row['azi'], beta),
                'east': compute_east(trajectory[-1]['east'], trajectory[-1]['md'], row['md'], trajectory[-1]['inc'], row['inc'], trajectory[-1]['azi'], row['azi'], beta),
                'tvd': compute_tvd(trajectory[-1]['tvd'], trajectory[-1]['md'], row['md'], trajectory[-1]['inc'], row['inc'], beta),
                # 'dls': degrees(beta)
                'dls': compute_dls(trajectory[-1]['md'], row['md'], beta)
            }
            trajectory.append(new_point)
    return pd.DataFrame(trajectory[1:])

def compute_beta(inc1, inc2, azi1, azi2):
    cos_value = cos(radians(inc2) - radians(inc1)) - sin(radians(inc1)) * sin(radians(inc2)) * (1 - cos(radians(azi2) - radians(azi1)))
    cos_value = max(min(cos_value, 1), -1)
    beta = acos(cos_value)
    return beta

def compute_north(north_prev, md1, md2, inc1, inc2, azi1, azi2, beta):
    rf = compute_rf(beta)
    delta_md = md2 - md1
    north_delta = 0.5 * delta_md * (sin(radians(inc1)) * cos(radians(azi1)) +
                                    sin(radians(inc2)) * cos(radians(azi2))) * rf
    return north_prev + north_delta

def compute_east(east_prev, md1, md2, inc1, inc2, azi1, azi2, beta):
    rf = compute_rf(beta)
    delta_md = md2 - md1
    east_delta = 0.5 * delta_md * (sin(radians(inc1)) * sin(radians(azi1)) +
                                   sin(radians(inc2)) * sin(radians(azi2))) * rf
    return east_prev + east_delta

def compute_tvd(tvd_prev, md1, md2, inc1, inc2, beta):
    rf = compute_rf(beta)
    delta_md = md2 - md1
    tvd_delta = 0.5 * delta_md * (cos(radians(inc1)) + cos(radians(inc2))) * rf
    return tvd_prev + tvd_delta

def compute_rf(beta):
    if beta == 0:
        return 1
    else:
        return (2 / beta) * tan(beta / 2)

def compute_dls(md1, md2, beta):
    delta_md = md2 - md1
    dls = (degrees(beta) / delta_md) * 100
    return dls

def plot_data(df, highlight_dls):
    if highlight_dls:
        custom_colorscale = [
            [0.0, 'rgba(220,218,218,255)'],
            [0.5, 'rgba(245,181,136,255)'],
            [1.0, 'rgba(179,13,29,255)']
        ]

        fig = go.Figure(
            data=[go.Scatter3d(
                x=df['east'],
                y=df['north'],
                z=df['tvd'],
                mode='markers',
                marker=dict(
                    size=5,
                    color=df['dls'],  # Color by dogleg severity
                    colorscale=custom_colorscale,
                    showscale=True,
                    opacity=1.0),
                hovertemplate='<b>MD</b>: %{customdata[0]:.2f}<br>' +
                              '<b>Inc</b>: %{customdata[1]:.2f}<br>' +
                              '<b>Azi</b>: %{customdata[2]:.2f}<br>' +
                              '<b>North</b>: %{y:.2f}<br>' +
                              '<b>East</b>: %{x:.2f}<br>' +
                              '<b>TVD</b>: %{z:.2f}<br>' +
                              '<b>DLS</b>: %{marker.color:.2f}<extra></extra>',
                customdata=df[['md', 'inc', 'azi']])
            ])
    else:
        fig = px.line_3d(df, x='east', y='north', z='tvd', color_discrete_sequence=['blue'])

    fig.update_layout(scene=dict(
        xaxis_title='East, ft',
        yaxis_title='North, ft',
        zaxis_title='TVD, ft',
        aspectmode='manual'),
        height=750)
    
    fig.update_scenes(zaxis_autorange='reversed')

    return fig

st.title('DLS Plotter')

raw_data = st.text_area(
    'data', placeholder='Paste date here', label_visibility='collapsed')

if raw_data:
    df = prep_data(raw_data)
    df = load_data(df)
    st.plotly_chart(plot_data(df, highlight_dls=True))
    st.dataframe(df, height=600, use_container_width=True)