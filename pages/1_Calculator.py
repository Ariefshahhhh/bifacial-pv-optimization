import streamlit as st

st.set_page_config(page_title="PV Performance Calculator", layout="wide")

st.title("⚡ PV Performance Calculator (Manual)")
st.markdown("Based on standard PV performance equations")

st.markdown("---")

# ===============================
# INPUT SECTION
# ===============================

col1, col2 = st.columns(2)

with col1:
    st.subheader("STC Electrical Parameters")

    Pstc = st.number_input("Pmax,STC (W)", value=470.0, format="%.3f")
    Vmp_stc = st.number_input("Vmp,STC (V)", value=38.0, format="%.3f")
    Imp_stc = st.number_input("Imp,STC (A)", value=12.23, format="%.3f")
    Voc_stc = st.number_input("Voc,STC (V)", value=46.8, format="%.3f")
    Isc_stc = st.number_input("Isc,STC (A)", value=12.89, format="%.3f")

with col2:
    st.subheader("Operating Conditions")

    Tc = st.number_input("Cell Temperature Tc (°C)", value=65.0, format="%.3f")
    fg = st.number_input("Irradiance factor fg", value=0.95, format="%.3f")
    fmm = st.number_input("Mismatch factor fmm", value=0.97, format="%.3f")
    fage = st.number_input("Aging factor fage", value=0.94, format="%.3f")
    fclean = st.number_input("Cleaning factor fclean", value=0.97, format="%.3f")
    funshade = st.number_input("Unshaded factor funshade", value=1.00, format="%.3f")

st.markdown("---")

st.subheader("Temperature Coefficients (from datasheet)")

col3, col4, col5 = st.columns(3)

with col3:
    alpha = st.number_input("α (Current coeff, %/°C)", value=0.048, format="%.3f")

with col4:
    beta = st.number_input("β (Voltage coeff, %/°C)", value=-0.283, format="%.3f")

with col5:
    gamma = st.number_input("γ (Power coeff, %/°C)", value=-0.360, format="%.3f")

# ===============================
# CALCULATION
# ===============================

if st.button("Calculate PV Performance"):

    # Temperature factors
    ftemp_p = 1 + (gamma / 100) * (Tc - 25)
    ftemp_i = 1 + (alpha / 100) * (Tc - 25)
    ftemp_v = 1 + (beta / 100) * (Tc - 25)

    # Power
    P = Pstc * fg * ftemp_p * fmm * fage * fclean * funshade

    # Current
    Imp = Imp_stc * ftemp_i * fg * fclean * funshade
    Isc = Isc_stc * ftemp_i * fg * fclean * funshade

    # Voltage
    Vmp = Vmp_stc * ftemp_v
    Voc = Voc_stc * ftemp_v

    st.markdown("---")
    st.subheader("Calculated Results")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Pmax (W)", f"{P:.2f}")
    c2.metric("Vmp (V)", f"{Vmp:.2f}")
    c3.metric("Imp (A)", f"{Imp:.2f}")
    c4.metric("Voc (V)", f"{Voc:.2f}")
    c5.metric("Isc (A)", f"{Isc:.2f}")

    # Save for ABC page
    st.session_state["P_calc"] = P
    st.session_state["Vmp_calc"] = Vmp
    st.session_state["Imp_calc"] = Imp
    st.session_state["Voc_calc"] = Voc
    st.session_state["Isc_calc"] = Isc
