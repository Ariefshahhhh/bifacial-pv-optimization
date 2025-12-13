import streamlit as st

st.set_page_config(page_title="PV Electrical Calculator", layout="wide")

st.title("🔆 Bifacial PV Electrical Output Calculator")
st.markdown("Manual calculation based on datasheet temperature coefficients and loss factors.")

st.markdown("---")

# ======================
# INPUT SECTION
# ======================
col1, col2 = st.columns(2)

with col1:
    st.subheader("PV Array & Environmental Data")

    Pmax_stc = st.number_input("Pmax at STC (W)", value=470.0)
    Vmp_stc  = st.number_input("Vmp at STC (V)", value=38.0)
    Imp_stc  = st.number_input("Imp at STC (A)", value=12.23)
    Voc_stc  = st.number_input("Voc at STC (V)", value=46.8)
    Isc_stc  = st.number_input("Isc at STC (A)", value=12.89)

    Ns = st.number_input("Modules in series (Ns)", value=30, step=1)
    Np = st.number_input("Modules in parallel (Np)", value=2, step=1)

    G = st.number_input("Irradiance G (W/m²)", value=950.0)
    Tc = st.number_input("Cell Temperature Tc (°C)", value=65.0)

with col2:
    st.subheader("Temperature Coefficients (Datasheet)")

    alpha = st.number_input("α (Current coeff %/°C)", value=0.048, format="%.3f")
    beta  = st.number_input("β (Voltage coeff %/°C)", value=-0.283, format="%.3f")
    gamma = st.number_input("γ (Power coeff %/°C)", value=-0.360, format="%.3f")

    st.subheader("Loss Factors")

    Fmm = st.number_input("Fmm (Mismatch)", value=0.97, format="%.3f")
    Fage = st.number_input("Fage (Aging)", value=0.94, format="%.3f")
    Fg = st.number_input("Fg (Irradiance)", value=0.95, format="%.3f")
    Fclean = st.number_input("Fclean", value=0.97, format="%.3f")
    Funshade = st.number_input("Funshade", value=1.00, format="%.3f")

# ======================
# CALCULATION SECTION
# ======================
st.markdown("---")

if st.button("Calculate Outputs"):

    # STC Array Values
    P_stc_array = Ns * Np * Pmax_stc
    Vmp_array_stc = Ns * Vmp_stc
    Imp_array_stc = Np * Imp_stc
    Voc_array_stc = Ns * Voc_stc
    Isc_array_stc = Np * Isc_stc

    # Temperature factors
    f_temp_p = 1 + (gamma / 100) * (Tc - 25)
    f_temp_i = 1 + (alpha / 100) * (Tc - 25)
    f_temp_v = 1 + (beta  / 100) * (Tc - 25)

    # Power
    Pmax = P_stc_array * Fmm * Fage * f_temp_p * Fg * Fclean * Funshade

    # Current
    Imp = Imp_array_stc * f_temp_i * Fg * Fclean * Funshade
    Isc = Isc_array_stc * f_temp_i

    # Voltage
    Vmp = Vmp_array_stc * f_temp_v
    Voc = Voc_array_stc * f_temp_v

    # ======================
    # OUTPUT SECTION
    # ======================
    st.subheader("📊 Calculated Results")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Pmax (W)", f"{Pmax:.2f}")
    c2.metric("Vmp (V)", f"{Vmp:.2f}")
    c3.metric("Imp (A)", f"{Imp:.2f}")
    c4.metric("Voc (V)", f"{Voc:.2f}")
    c5.metric("Isc (A)", f"{Isc:.2f}")

    # Save for next pages
    st.session_state["P_calculated"] = Pmax
    st.session_state["Vmp"] = Vmp
    st.session_state["Imp"] = Imp
    st.session_state["Voc"] = Voc
    st.session_state["Isc"] = Isc
