import streamlit as st
import pandas as pd
import well_profile as wp
import utilities

st.title('test2')

data = st.text_area('data')


df = prep_df(create_df(data))
st.write(df)


##############################

# df = pd.DataFrame([[0, 0, 0]], columns=["md", "inc", "azi"])
# data = st.data_editor(df)

# options = {
#     'tvd': ['A', 'B'],
#     'hlt': ['A', 'B']
# }

# label_visibility = 'collapsed'

# tvd = st.selectbox(
#     'tvd', options['tvd'], label_visibility=label_visibility)

# hl = st.selectbox(
#     'hlt', options['hlt'], label_visibility=label_visibility)

# data = st.text_area('data')


# def convert_to_csv(input_string):
#     values = input_string.split()
#     # Group every three values
#     grouped_values = [values[i:i + 3] for i in range(0, len(values), 3)]
#     df = pd.DataFrame(grouped_values, columns=['md', 'inc', 'azi'])
#     return df

# # df = convert_to_csv(data)
# # st.write(df)

# # wp = wp.load(df)
# # st.plotly_chart(wp.plot(style={'color': 'dls', 'size': 5}))

# # wp.plot(style={'color': 'dls', 'size': 5}).show()
