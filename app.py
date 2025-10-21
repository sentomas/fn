import streamlit as st
import numpy as np
import plotly.express as px

# --- Header / intro ---
st.set_page_config(page_title="SDOF Natural Frequency — Damping", layout="wide", initial_sidebar_state="auto")
st.title("SDOF Natural Frequency Calculator")
st.subheader("Single Degree of Freedom (SDOF) system — includes damping")
st.markdown(
    "Use the controls below to set stiffness, mass and damping. "
    "Results show undamped and damped natural frequencies, critical damping and damping ratio."
)
st.info("For customized development or further assistance, write to: [services@serinthomas.in](mailto:services@serinthomas.in)")

# --- Inputs in a compact, professional layout ---
with st.container():
    col_k, col_m, col_c = st.columns([1, 1, 1])
    with col_k:
        k = st.number_input("Stiffness k (N/m)", min_value=0.01, value=500.0, format="%.3f")
    with col_m:
        m = st.number_input("Mass m (kg)", min_value=0.01, value=10.0, format="%.3f")
    with col_c:
        c = st.number_input("Damping c (N·s/m)", min_value=0.0, value=1.0, format="%.3f")

# --- Calculations ---
omega_n = np.sqrt(k / m)              # rad/s
f_n = omega_n / (2 * np.pi)          # Hz

c_crit = 2 * np.sqrt(k * m)
zeta = c / c_crit if c_crit > 0 else 0.0

if zeta < 1.0:
    omega_d = omega_n * np.sqrt(1.0 - zeta**2)
    f_d = omega_d / (2 * np.pi)
else:
    f_d = 0.0

# --- Results as metrics ---
res_col1, res_col2, res_col3, res_col4 = st.columns(4)
res_col1.metric("Undamped freq (Hz)", f"{f_n:.3f}")
res_col2.metric("Damped freq (Hz)", f"{f_d:.3f}" if zeta < 1.0 else "—")
res_col3.metric("Damping ratio ζ", f"{zeta:.4f}")
res_col4.metric("Critical damping c_cr (N·s/m)", f"{c_crit:.3g}")

st.markdown(
    ("**Notes:**\n\n"
     "- If ζ ≥ 1 the system is critically/over-damped and will not oscillate (damped frequency not defined).\n"
     "- Values update instantly when inputs change.")
)

# --- Plots in expanders to keep layout tidy ---
with st.expander("Frequency vs Mass"):
    mass_values = np.linspace(0.1, 50, 300)
    freq_vs_mass = (1 / (2 * np.pi)) * np.sqrt(k / mass_values)
    zeta_mass = c / (2 * np.sqrt(k * mass_values))
    damped_factor_mass = np.sqrt(np.clip(1.0 - zeta_mass**2, 0.0, None))
    freq_damped_mass = freq_vs_mass * damped_factor_mass

    fig1 = px.line(x=mass_values, y=freq_vs_mass, labels={'x': 'Mass (kg)', 'y': 'Frequency (Hz)'}, title='Undamped and Damped Frequency vs Mass')
    fig1.add_scatter(x=mass_values, y=freq_damped_mass, mode='lines', name='Damped Frequency')
    st.plotly_chart(fig1, use_container_width=True)

with st.expander("Frequency vs Stiffness"):
    stiffness_values = np.linspace(max(1.0, k * 0.02), max(100.0, k * 3.0), 300)
    freq_vs_stiffness = (1 / (2 * np.pi)) * np.sqrt(stiffness_values / m)
    zeta_stiff = c / (2 * np.sqrt(stiffness_values * m))
    damped_factor_stiff = np.sqrt(np.clip(1.0 - zeta_stiff**2, 0.0, None))
    freq_damped_stiff = freq_vs_stiffness * damped_factor_stiff

    fig2 = px.line(x=stiffness_values, y=freq_vs_stiffness, labels={'x': 'Stiffness (N/m)', 'y': 'Frequency (Hz)'}, title='Undamped and Damped Frequency vs Stiffness')
    fig2.add_scatter(x=stiffness_values, y=freq_damped_stiff, mode='lines', name='Damped Frequency')
    st.plotly_chart(fig2, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.caption("Professional services: For customized development or support email services@serinthomas.in")