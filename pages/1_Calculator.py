import streamlit as st

st.title("⚡ Bifacial PV Output Computation Tool")
st.markdown(
    "Compute **Maximum Power (Pmax)**, **Vmp**, **Imp**, **Voc**, and **Isc** "
    "based strictly on datasheet values and standard PV correction formulas."
)
st.markdown("---")

# =========================
# INPUT LAYOUT
# =========================
col1, col2 = st.columns(2)

# ---------- LEFT ----------
with col1:
    st.subheader("📦 STC Electrical Parameters")

    P_stc = st.number_input("Rated Power at STC, Pstc (W)", value=600.0)
    I_stc = st.number_input("Current at Maximum Power, Istc (A)", value=15.0)
    V_stc = st.number_input("Voltage at Maximum Power, Vstc (V)", value=40.0)
    Isc_stc = st.number_input("Short Circuit Current, Isc_STC (A)", value=15.8)
    Voc_stc = st.number_input("Open Circuit Voltage, Voc_STC (V)", value=48.5)

    Tmod = st.number_input("Module Temperature, Tmod (°C)", value=45.0)

# ---------- RIGHT ----------
with col2:
    st.subheader("🌡 Temperature Coefficients (Datasheet)")

    alpha = st.number_input("α (Isc coefficient, %/°C)", value=0.045, format="%.3f")
    beta  = st.number_input("β (Voc coefficient, %/°C)", value=-0.230, format="%.3f")
    gamma = st.number_input("γ (Pmax coefficient, %/°C)", value=-0.280, format="%.3f")

    st.subheader("⚙ Correction Factors")

    Fg       = st.number_input("Glass / Soiling Factor, Fg", value=0.95, min_value=0.80, max_value=1.00)
    Fclean   = st.number_input("Cleaning Factor, Fclean", value=0.97, min_value=0.80, max_value=1.00)
    Funshade = st.number_input("Unshaded Factor, Funshade", value=1.00, min_value=0.80, max_value=1.00)
    Fmm      = st.number_input("Mismatch Factor, Fmm", value=0.98, min_value=0.80, max_value=1.00)
    Fdegrad  = st.number_input("Degradation Factor, Fdegrad", value=0.95, min_value=0.80, max_value=1.00)

# =========================
# CALCULATION
# =========================
if st.button("Calculate Outputs"):

    # Temperature correction factors
    Ftemp_I = 1 + (alpha / 100) * (Tmod - 25)
    Ftemp_V = 1 + (beta  / 100) * (Tmod - 25)
    Ftemp_P = 1 + (gamma / 100) * (Tmod - 25)

    # Outputs based on given formula
    Pmax = P_stc * Ftemp_P * Fg * Fclean * Funshade * Fmm * Fdegrad
    Imp  = I_stc * Ftemp_I * Fg * Fclean * Funshade
    Vmp  = V_stc * Ftemp_V
    Isc  = Isc_stc * Ftemp_I * Fg * Fclean * Funshade
    Voc  = Voc_stc * Ftemp_V

    st.markdown("---")
    st.subheader("📊 Computed Electrical Outputs")

    colA, colB = st.columns(2)

    with colA:
        st.success(f"**Maximum Power, Pmax** = {Pmax:.2f} W")
        st.success(f"**Voltage at Maximum Power, Vmp** = {Vmp:.2f} V")
        st.success(f"**Open Circuit Voltage, Voc** = {Voc:.2f} V")

    with colB:
        st.success(f"**Current at Maximum Power, Imp** = {Imp:.2f} A")
        st.success(f"**Short Circuit Current, Isc** = {Isc:.2f} A")

    st.info("All results are computed strictly according to standard PV correction equations.")
