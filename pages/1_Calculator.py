import streamlit as st

st.title("⚡ Bifacial PV Output Computation Tool")
st.markdown("Compute Pout, Vmp, Imp, Voc, and Isc with full temperature correction and loss factors.")
st.markdown("---")

# Layout for inputs
col1, col2 = st.columns(2)

# ---------- LEFT SIDE ----------
with col1:
    st.subheader("🔆 Environmental Inputs")

    G_front = st.number_input("Front Irradiance (W/m²)", value=800.0)
    G_rear = st.number_input("Rear Irradiance (W/m²)", value=100.0)
    Tcell = st.number_input("Cell Temperature (°C)", value=30.0)

    st.subheader("📦 Module STC Electrical Data")
    Pmax_stc = st.number_input("Pmax at STC (W)", value=450.0)
    Vmp_stc = st.number_input("Vmp at STC (V)", value=41.0, step=0.1)
    Imp_stc = st.number_input("Imp at STC (A)", value=10.98, step=0.01)
    Voc_stc = st.number_input("Voc at STC (V)", value=49.5, step=0.1)
    Isc_stc = st.number_input("Isc at STC (A)", value=11.5, step=0.01)

# ---------- RIGHT SIDE ----------
with col2:
    st.subheader("🌡 Temperature Coefficients")
    alpha = st.number_input("α (Isc Temperature Coefficient, 1/°C)", value=0.040, format="%.3f")
    beta = st.number_input("β (Voc Temperature Coefficient, 1/°C)", value=-0.280, format="%.3f")
    gamma = st.number_input("γ (Pmax Temperature Coefficient, 1/°C)", value=-0.350, format="%.3f")

    st.subheader("⚙ Correction Factors")
    Fmm = st.number_input("Mismatch Factor (Fmm)", value=0.98, min_value=0.80, max_value=1.00, step=0.01)
    Fage = st.number_input("Aging Factor (Fage)", value=0.95, step=0.01, min_value=0.80, max_value=1.00)
    Fg = st.number_input("Glass/Soiling Factor (Fg)", value=0.97, step=0.01, min_value=0.80, max_value=1.00)
    Fclean = st.number_input("Cleaning Factor (Fclean)", value=0.98, step=0.01, min_value=0.80, max_value=1.00)
    Fshade = st.number_input("Shading Factor (Fshade0", value=0.95, step=0.01, min_value=0.80, max_value=1.00)

# ----- CALCULATE BUTTON -----
if st.button("Calculate Outputs"):
    G_total = G_front + G_rear

    # Temperature adjusted values
    Isc_T = Isc_stc * (1 + alpha * (Tcell - 25))
    Voc_T = Voc_stc * (1 + beta * (Tcell - 25))
    Pmax_T = Pmax_stc * (1 + gamma * (Tcell - 25))

    # Effective output power
    Pout = (
        Pmax_T *
        (G_total / 1000) *
        Fmm *
        Fage *
        Fg *
        Fclean *
        Fshade
    )

    # Vmp & Imp temperature corrections (approx model)
    Vmp_T = Vmp_stc * (1 + beta * (Tcell - 25))
    Imp_T = Pout / Vmp_T if Vmp_T != 0 else 0

    # Display results
    st.markdown("---")
    st.subheader("📊 Calculated Electrical Outputs")

    colA, colB = st.columns(2)
    with colA:
        st.success(f"**Pout** = {Pout:.2f} W")
        st.success(f"**Vmp** = {Vmp_T:.2f} V")
        st.success(f"**Voc** = {Voc_T:.2f} V")

    with colB:
        st.success(f"**Imp** = {Imp_T:.2f} A")
        st.success(f"**Isc** = {Isc_T:.2f} A")

    # SAVE to session_state for ABC optimization
    st.session_state["P_calculated"] = Pout
    st.session_state["Isc_T"] = Isc_T
    st.session_state["Voc_T"] = Voc_T
    st.session_state["Vmp_T"] = Vmp_T
    st.session_state["Imp_T"] = Imp_T
    st.session_state["G_total"] = G_total
    st.session_state["Pmax_T"] = Pmax_T
    st.session_state["Pmax_stc"] = Pmax_stc
    st.session_state["temp_coeff_gamma"] = gamma

    st.info("Values saved. You may proceed to the ABC Optimization page.")
