import streamlit as st
import pandas as pd
from math import degrees, radians, cos, sin, acos, tan
import plotly.express as px
import plotly.graph_objects as go

def prepare_trajectory_data(input_string):
    # Split string and group every three values
    values = input_string.split()
    grouped_values = [values[i:i + 3] for i in range(0, len(values), 3)]

    # Create DataFrame and convert columns to numeric, dropping NaNs
    df = pd.DataFrame(grouped_values, columns=['md', 'inc', 'azi'])
    df = df.apply(pd.to_numeric, errors='coerce').dropna()
    return df

def calculate_trajectory(data):
    # Initialize trajectory with starting point
    trajectory = [{'md': 0, 'inc': 0, 'azi': 0, 'dls': 0, 'tvd': 0, 'north': 0, 'east': 0}]
    
    for index, row in data.iterrows():
        if row['md'] > 0:
            last_point = trajectory[-1]
            dogleg = calculate_dogleg(last_point['inc'], row['inc'], last_point['azi'], row['azi'])
            new_point = calculate_new_point(last_point, row, dogleg)
            trajectory.append(new_point)
    
    return pd.DataFrame(trajectory[1:])  # Skip the initial dummy point

def calculate_dogleg(inc1, inc2, azi1, azi2):
    # Dogleg calculation based on inclination and azimuth
    if inc1 == inc2 and azi1 == azi2:
        return 0
    inner_value = cos(radians(inc1)) * cos(radians(inc2)) + \
                  sin(radians(inc1)) * sin(radians(inc2)) * cos(radians(azi2 - azi1))
    inner_value = max(min(inner_value, 1), -1)  # Clamping between -1 and 1
    return acos(inner_value)

def calculate_new_point(last_point, current_point, dogleg):
    # Calculation of new trajectory point
    rf = calculate_rf(dogleg)
    delta_md = current_point['md'] - last_point['md']
    return {
        'md': current_point['md'],
        'inc': current_point['inc'],
        'azi': current_point['azi'],
        'north': last_point['north'] + calculate_delta(delta_md, last_point['inc'], current_point['inc'], last_point['azi'], current_point['azi'], rf, 'north'),
        'east': last_point['east'] + calculate_delta(delta_md, last_point['inc'], current_point['inc'], last_point['azi'], current_point['azi'], rf, 'east'),
        'tvd': last_point['tvd'] + calculate_delta(delta_md, last_point['inc'], current_point['inc'], rf=rf, axis='tvd'),
        'dls': degrees(dogleg)
    }

def calculate_delta(delta_md, inc1, inc2, azi1=None, azi2=None, rf=None, axis='north'):
    # Helper function to calculate north, east, and tvd delta
    if axis == 'north' or axis == 'east':
        return 0.5 * delta_md * (sin(radians(inc1)) * cos(radians(azi1)) + sin(radians(inc2)) * cos(radians(azi2))) * rf
    elif axis == 'tvd':
        return 0.5 * delta_md * (cos(radians(inc1)) + cos(radians(inc2))) * rf

def calculate_rf(dogleg):
    # Calculate ratio factor (RF) based on dogleg
    return 1 if dogleg == 0 else tan(dogleg / 2) / (dogleg / 2)

def plot_trajectory(df, highlight_dls):
    # Plotting function with optional highlighting of dogleg severity
    fig = create_plot_figure(df, highlight_dls)
    fig.update_layout(scene=dict(
        xaxis_title='East, ft',
        yaxis_title='North, ft',
        zaxis_title='TVD, ft',
        aspectmode='manual'),
        height=750)
    fig.update_scenes(zaxis_autorange='reversed')
    return fig

def create_plot_figure(df, highlight_dls):
    # Function to create plot figure
    if highlight_dls:
        custom_colorscale = [[0.0, 'rgba(220,218,218,255)'], [0.5, 'rgba(245,181,136,255)'], [1.0, 'rgba(179,13,29,255)']]
        return go.Figure(data=[create_scatter3d(df, custom_colorscale)])
    else:
        return px.line_3d(df, x='east', y='north', z='tvd', color_discrete_sequence=['blue'])

def create_scatter3d(df, custom_colorscale):
    # Helper function to create Scatter3D plot
    return go.Scatter3d(
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
        customdata=df[['md', 'inc', 'azi']]
    )

# Streamlit UI setup
st.title('Dogleg Severity Plotter')
raw_data = st.text_area('data', placeholder='Paste data here', label_visibility='collapsed')

if raw_data:
    df = prepare_trajectory_data(raw_data)
    df = calculate_trajectory(df)
    st.plotly_chart(plot_trajectory(df, highlight_dls=True))
    st.dataframe(df, height=600, use_container_width=True)
