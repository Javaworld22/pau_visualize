import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

from raceplotly.plots import barplot
from PIL import Image
import time
import sys


st.title("Executive Summary: Our Solution Dashboard")
image1 = Image.open('dashboard1.PNG')
st.image(image1, caption='Dashboard', use_container_width=True)

image2 = Image.open('dashboard.PNG')
st.image(image2, caption='Dedicated User Portal predefined Locations', use_container_width=True)

st.title("PAU Energy consumption")
st.write("Below are Energy readings for PAU from Sapt 2024 through Sept 2024 and August 2025 through September 2025.")

#df = pd.DataFrame({
#    "Category": ["0", "1", "2", "3","4","5","6","7","8", "9", "10","11","12","13","14",
#                 "15","16","17","18","19","20","21","22","23"] * 30,
#    "Value": np.random.randint(10, 100, 720),
#    "Year": sorted(list(range(1, 31)) * 24)
#})
#st.write(df)

if "mbar" not in st.session_state:
    st.session_state.mbar = 0
if "mnth" not in st.session_state:
    st.session_state.mnth = 0
if "mStages" not in st.session_state:
    st.session_state.mStages = 0
    
st.session_state.mdata = 0
if "name1" not in st.session_state:
    st.session_state.name1 = "June"

if "name2" not in st.session_state:
    st.session_state.name2 = "July"

df1 = pd.read_csv("energy_pau.csv")
df_2025_sept = pd.read_csv("energy_pau_sept.csv")
df_2024 = pd.read_csv("energy_pau_2024.csv")
df_2024_sept = pd.read_csv("energy_pau_2024_sept.csv")





# Create the animated chart with Plotly Express
#fig = px.bar(
#    df,
#    x="Category",
#    y="Value",
#    color="Category",
#    animation_frame="Year",
#    animation_group="Category",
#    title="Yearly Performance",
#    height=500
#)

# Display the chart in Streamlit
#st.plotly_chart(fig, use_container_width=True)


def move_2025():
    """Decrement the year index, preventing it from going below zero."""
    if st.session_state.mbar == 0:
        st.session_state.mbar = 1
        st.session_state.name1 = "Aug"
        st.session_state.name2 = "Sept"
        

def move_2024():
    """Increment the year index, preventing it from exceeding the maximum."""
    if st.session_state.mbar == 1:
        st.session_state.mbar = 0
        st.session_state.name1 = "June"
        st.session_state.name2 = "July"
        #if st.session_state.mbar == 0 and st.session_state.mnth == 0:
         #   mdata = df_2024
        #elif st.session_state.mbar == 0 and st.session_state.mnth == 1:
         #   mdata = df_2024_sept

def move_1():
    """Increment the year index, preventing it from exceeding the maximum."""
    if st.session_state.mnth == 0:
        st.session_state.mnth = 1
        #st.session_state.mbar == 0
       

def move_2():
    """Increment the year index, preventing it from exceeding the maximum."""
    if st.session_state.mnth == 1:
        st.session_state.mnth = 0
       

col1_1, col2_2, _,col3,col4 = st.columns([1, 1,4,1,1])
#col3, col4, _ = st.columns([1, 1,8])
mdata = None
with col1_1:
    st.button("2024", on_click=move_2024)

with col2_2:
    st.button("2025", on_click=move_2025)

with col3:
    st.button(st.session_state.name1, on_click=move_1)

with col4:
    st.button(st.session_state.name2, on_click=move_2)

if st.session_state.mbar == 0 and st.session_state.mnth == 0:
    mdata = df_2024_sept
    st.session_state.mStages = 1
elif st.session_state.mbar == 0 and st.session_state.mnth == 1:
    mdata = df_2024
    st.session_state.mStages = 2
elif st.session_state.mbar == 1 and st.session_state.mnth == 0:
    mdata = df_2025_sept
    st.session_state.mStages = 3
elif st.session_state.mbar == 1 and st.session_state.mnth == 1:
    mdata = df1
    st.session_state.mStages = 4

#st.write(mdata)

# Initialize the bar plot race
my_raceplot = barplot(
    df= mdata,
    item_column='hr',
    value_column='diff',
    time_column='day',
    top_entries=24
)

# Generate the race plot figure
race_fig = my_raceplot.plot(
    title='Bar Chart Race',
    item_label='hr',
    value_label='Energy Consumption in (KWh)',
    frame_duration=1000,
    orientation='vertical' # This is the key parameter
)

fig = my_raceplot.fig

# 4. Update the layout of the figure to change background colors
fig.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0.1)',  # Color of the plot area (behind the bars)
    paper_bgcolor='rgba(0, 0, 0, 0.1)'   # Color of the entire figure area (including margins)
)

#st.set_page_config(layout="wide")
# Display the plot in Streamlit
st.plotly_chart(fig, use_container_width=True)

if  st.session_state.mStages == 2:
    st.write("Extremely High Usage: Recorded daily consumption was exceptionally high, ranging from an estimated 700 to 900 kWh on full days. For context, this is many times higher than a typical household.")
    st.write("Significant Spike: The most notable event was a massive 77 kWh spike at 7 PM on June 25th, indicating a singular, high-power event like powering heating elements or higher inductive loads.")
    st.write("")
elif st.session_state.mStages == 1:
    st.markdown("""
    **1. Extremely High Hourly Consumption**: Energy use is consistently high throughout the day and night.
    * Overnight (Midnight-6 AM): Consumption ranges from 16 to 30 kWh per hour.
    - Daytime (8 AM-6 PM): Consumption peaks, frequently reaching 30 to 41 kWh per hour.
    + The highest single hour recorded is 47 kWh at 5 AM on July 2nd, which is an unusual and massive spike for the early morning.
    """)
    st.markdown("""
     **2. Stable Baseline Load**: The constant high consumption (rarely dropping below 20 kWh in any hour) suggests a high baseline load. This implies that major equipment is running continuously, such as:
    * Industrial machinery (Inductive Loads)
    * Heating elements or filaments
    * The 47 kWh spike in the early morning of July 2nd is a significant anomaly that likely represents a specific high-power process starting up.
    """)
elif st.session_state.mStages == 4:
    st.markdown("""
     Average (Mean) Consumption (~25.2 kWh): This is the mathematical average of all hourly consumption values for August.
    """)
    st.markdown("""
     Average (Mean) Consumption (~25.2 kWh): This is the mathematical average of all hourly consumption values for August
    """)
    st.markdown("""
     Maximum Consumption (89 kWh): This was the highest amount of energy used in a single hour during August. This peak occurred twice:
     + August 20 at 3:00 PM (15:00)
     + August 25 at 1:00 PM (13:00)
     N/B: This very large range confirms that August's energy use was highly volatile, switching between periods of no use and very intense use.
    """)
    try:
        mg = pd.read_csv("energy_first.csv")
        st.dataframe(mg)
    except Exception as e:
        st.error(f"An error occurred while reading the CSV file: {e}")
    st.markdown("""
    + Peak EneAverage Energy: 24.6
    + Average Energy: 24.6
    + Daily Energy Consumption: 16,933.0 total across all periods
    + Standard Deviation: 16.7
    + Variance: 277.7

    """)
    
        
        
    
elif st.session_state.mStages == 3:
    st.markdown("""
    High Spikes: Significant spikes in usage, such as a 55 kWh draw at 8:00 AM on Sept 1st and a 41 kWh draw at 8:00 PM that same day.
    Low Consumption: Periods of very low or zero usage (e.g., 0 kWh at 2:00 AM, 5 kWh at 6:00 AM, 7 kWh at 10:00 PM).
    """)



#data = {'Category': ['A', 'B', 'C', 'D'],
#        'Value': [25, 35, 20, mday],
#         'Day':  [100, 200, 300, 150]
#        }
#df = pd.DataFrame(data)



# Get unique years and sort them
years =  sorted(list(range(1, 31))) #sorted(df['Day'].unique())
max_index = len(years) - 1

# Initialize session state for the current year index if it doesn't exist
if "year_index" not in st.session_state:
    st.session_state.year_index = 0

# --- Functions for button callbacks ---
def move_forward():
    """Increment the year index, preventing it from exceeding the maximum."""
    if st.session_state.year_index < max_index:
        st.session_state.year_index += 1

def move_backward():
    """Decrement the year index, preventing it from going below zero."""
    if st.session_state.year_index > 0:
        st.session_state.year_index -= 1

# --- Layout the buttons and chart ---
# Use columns to place the buttons side-by-side
col1, col2, _ = st.columns([1, 1, 6])

with col1:
    st.button("Backward", on_click=move_backward, disabled=(st.session_state.year_index == 0))

with col2:
    st.button("Forward", on_click=move_forward, disabled=(st.session_state.year_index == max_index))

# Get the current year based on the index
current_year = years[st.session_state.year_index]
filtered_df = df[df['Day'] == current_year]

#data = {'Category': ['A', 'B', 'C', 'D'],
#        'Value': [25, 35, 20, current_year],
#         'Day':  [100, 200, 300, 150]
#        }
#df = pd.DataFrame(data)

mCount = 0
mday = {}
energy_day = []
for i in range(32):
    for x in df1.index:
        if df1.loc[x, 'day'] == i:
            mCount = mCount + df1.loc[x, 'diff']
    mday.update({'day':i, 'Energy':mCount})
    if mday["Energy"] != 0:
        energy_day.append(mday)
    mday = {}
    mCount = 0
#st.write(energy_day)

df = pd.DataFrame(energy_day)
mexplode = [0.2,0.1,0.1,0.3,0.1]
for i in energy_day:
    mexplode.append(np.random.uniform(0,0.3))


# Create and display the pie chart
fig = go.Figure(
    data=[go.Pie(
        values=df['Energy'],  #filtered_df['Value']
        labels=df['day'] , #filtered_df['Category']
        hole=0.5,
        pull=mexplode
    )]
)

# Create a donut chart
#fig = px.pie(df, values='Value', names='Category', hole=0.5,
#             title='Animated Donut Chart')

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)

#st.write(filtered_df['Value'])


mday = (1, 2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31)
st.selectbox("Select Day", mday)        


mMonth = ("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sept","Oct","Nov","Dec")
st.selectbox("Select Month", mMonth)

















