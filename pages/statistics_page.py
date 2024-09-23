import streamlit as st
from src.data.statistics import *

st.markdown("# Estatistics ❄️")
st.sidebar.markdown("# Estatistics ❄️")

# Load your dataset
df = get_dataset()



# ------------------------------------------------
st.title('General Traffic Accident Statistics')

# Call the general_statistics function to get the data
general_stats = general_statistics(df)

st.metric("Total Accidents", general_stats['Total Accidents'])
st.metric("Total Deaths", general_stats['Total Deaths'])
st.metric("Total Minor Injuries", general_stats['Total Minor Injuries'])
st.write(f"Dataset Time Period: {general_stats['Dataset Time Period']}")
st.metric("Fatality Rate (%)", general_stats['Fatality Rate (%)'])



# ------------------------------------------------
st.title('Accident Severity Statistics')

# Get accident severity statistics
severity_df = accident_severity(df)

# Plotting the severity levels using Streamlit
st.bar_chart(severity_df.set_index('Severity'))



# ------------------------------------------------
st.title("Traffic Accident Analysis")

# Get statistics
cause_df = main_causes(df)
classification_df = accident_classification(df)
type_df = common_accident_types(df)

# Main Causes
st.subheader("Main Causes of Accidents")
st.bar_chart(cause_df.set_index('Cause'))

# Classification of Accidents
st.subheader("Accident Classification")
st.bar_chart(classification_df.set_index('Classification'))

# Common Types of Accidents
st.subheader("Common Types of Accidents")
st.bar_chart(type_df.set_index('Accident Type'))



# ------------------------------------------------
st.title("Environmental Conditions Analysis")

# Get environmental condition statistics
weather_df = weather_conditions(df)
direction_df = road_direction(df)
type_df = road_type(df)

# Weather Conditions
st.subheader("Weather Conditions")
st.bar_chart(weather_df.set_index('Weather Condition'))

# Road Direction
st.subheader("Road Direction")
st.bar_chart(direction_df.set_index('Road Direction'))

# Road Type
st.subheader("Road Type")
st.bar_chart(type_df.set_index('Road Type'))