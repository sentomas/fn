import streamlit as st
import numpy as np
import plotly.express as px

# Title
st.title("Natural Frequency Calculator for SDOF System")

# User inputs
k = st.number_input("Enter stiffness (k) in N/m:", min_value=0.01, value=500.0)
m = st.number_input("Enter mass (m) in kg:", min_value=0.01, value=10.0)

# Calculate natural frequency
f_n = (1 / (2 * np.pi)) * np.sqrt(k / m)

# Display result
st.markdown(f"### Natural Frequency: {f_n:.2f} Hz")

# Plot frequency vs mass
mass_values = np.linspace(0.1, 50, 100)
freq_vs_mass = (1 / (2 * np.pi)) * np.sqrt(k / mass_values)
fig1 = px.line(x=mass_values, y=freq_vs_mass, labels={'x': 'Mass (kg)', 'y': 'Frequency (Hz)'}, title='Frequency vs Mass')
st.plotly_chart(fig1)

# Plot frequency vs stiffness
stiffness_values = np.linspace(10, 1000, 100)
freq_vs_stiffness = (1 / (2 * np.pi)) * np.sqrt(stiffness_values / m)
fig2 = px.line(x=stiffness_values, y=freq_vs_stiffness, labels={'x': 'Stiffness (N/m)', 'y': 'Frequency (Hz)'}, title='Frequency vs Stiffness')
st.plotly_chart(fig2)