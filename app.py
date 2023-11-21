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

    # Create a DataFrame from the grouped values
    df = pd.DataFrame(grouped_values, columns=['a', 'b', 'c'])

    # # Export DataFrame to CSV file
    # df.to_csv('output.csv', index=False)


st.write(convert_to_csv(data))


# def input_to_csv(input_string):
#     # Convert string to StringIO object (which behaves like a file object)
#     string_io = StringIO(input_string)

#     # Read the string as a CSV into a DataFrame
#     df = pd.read_csv(string_io, sep=",")

#     # Export DataFrame to CSV file
#     df.to_csv("output.csv", index=False)

# st.write(data)

