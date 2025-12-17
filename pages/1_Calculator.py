import streamlit as st

st.title("⚡ Bifacial PV Output Computation Tool")
st.markdown("Computation of **Pmax, Vmp, Imp, Voc, Isc** using datasheet-based bifacial PV formulas.")
st.markdown("---")

col1, col2 = st.columns(2)

# ---------------- LEFT ----------------
with col1:
    st.subheader("🔆 Irradiance & Temperature")

    G_front = st.number_input("Front Irradiance, G_front (W/m²)", value=800.0)
    G_rear  = st.number_input("Rear Irradiance, G_rear (W/m²)", value=120.0)
    BG      = st.number_input("Bifacial Gain Factor (BG)", value=0.70, format="%.2f")
    Tmod    = st.number_input("Module Temperature, Tmod (°C)", value=45.0)

    st.subheader("📄 Datasheet Values at STC")

    P_stc  = st.number_input("Pmax_STC (W)", value=610.0)
    Vmp_stc = st.number_input("Vmp_STC (V)", value=40.61)
    Imp_stc = st.number_input("Imp_STC (A)", value=15.01)
    Voc_stc = st.number_input("Voc_STC (V)", value=48.48)
    Isc_stc = st.number_input("Isc_STC (A)", value=15.80)

# ---------------- RIGHT ----------------
with col2:
    st.subheader("🌡 Temperature Coefficients")

    alpha = st.number_input("α (Isc coefficient, %/°C)", value=0.045, format="%.3f")
    beta  = st.number_input("β (Voc coefficient, %/°C)", value=-0.230, format="%.3f")
    gamma = st.number_input("γ (Pmax coefficient, %/°C)", value=-0.280, format="%.3f")

    st.subheader("⚙ Loss Factors")

    Fclean   = st.number_input("Cleaning Factor, Fclean", value=0.98)
    Funshade = st.number_input("Unshaded Factor, Funshade", value=1.00)
    Fmm      = st.number_input("Mismatch Factor, Fmm", value=0.98)
    Fage     = st.number_input("Aging Factor, Fage", value=0.95)

# ---------------- CALCULATION ----------------
if st.button("Calculate Electrical Outputs"):

    # Effective bifacial irradiance
    G_eff = G_front + BG * G_rear
    Fg = G_eff / 1000

    # Temperature factors
    Ftemp_I = 1 + (alpha/100)*(Tmod - 25)
    Ftemp_V = 1 + (beta/100)*(Tmod - 25)
    Ftemp_P = 1 + (gamma/100)*(Tmod - 25)

    # Outputs
    Pmax = P_stc * Ftemp_P * Fg * Fclean * Funshade * Fmm * Fage
    Imp  = Imp_stc * Ftemp_I * Fg * Fclean * Funshade
    Vmp  = Vmp_stc * Ftemp_V
    Isc  = Isc_stc * Ftemp_I * Fg * Fclean * Funshade
    Voc  = Voc_stc * Ftemp_V

    st.markdown("---")
    st.subheader("📊 Computed Outputs (Bifacial PV)")

    colA, colB = st.columns(2)
    with colA:
        st.success(f"**Maximum Power, Pmax** = {Pmax:.2f} W")
        st.success(f"**Voltage at Pmax, Vmp** = {Vmp:.2f} V")
        st.success(f"**Open Circuit Voltage, Voc** = {Voc:.2f} V")

    with colB:
        st.success(f"**Current at Pmax, Imp** = {Imp:.2f} A")
        st.success(f"**Short Circuit Current, Isc** = {Isc:.2f} A")
