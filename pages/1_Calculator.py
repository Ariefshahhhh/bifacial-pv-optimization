import streamlit as st

st.title("⚡ Bifacial PV Electrical Computation Tool")
st.markdown("Calculate Pout, Voc, Isc, Vmp, and Imp with temperature correction and full factor adjustments.")
st.markdown("---")

# ------------ INPUT SECTION ------------
col1, col2 = st.columns(2)

with col1:
    Pmax_stc = st.number_input("Pmax at STC (W)", value=450.0)
    Voc_stc = st.number_input("Voc at STC (V)", value=50.0)
    Isc_stc = st.number_input("Isc at STC (A)", value=10.0)

    irr_front = st.number_input("Front Irradiance (W/m²)", value=800.0)
    irr_rear = st.number_input("Rear Irradiance (W/m²)", value=100.0)
    Tcell = st.number_input("Cell Temperature (°C)", value=30.0)

with col2:
    gammaP = st.number_input("γPmax (Power Temp Coefficient) [%/°C]", value=-0.350, format="%.3f")
    gammaVoc = st.number_input("βVoc (Voc Temp Coefficient) [%/°C]", value=-0.250, format="%.3f")
    gammaIsc = st.number_input("αIsc (Isc Temp Coefficient) [%/°C]", value=0.040, format="%.3f")

    Fmm = st.number_input("Mismatch Factor (Fmm)", value=0.980, min_value=0.800, max_value=1.000, step=0.001, format="%.3f")
    Fage = st.number_input("Aging Factor (Fage)", value=0.950, min_value=0.800, max_value=1.000, step=0.001, format="%.3f")
    Fg = st.number_input("Glass/Soiling Factor (Fg)", value=0.970, min_value=0.800, max_value=1.000, step=0.001, format="%.3f")
    Fclean = st.number_input("Cleaning Factor (Fclean)", value=0.980, min_value=0.800, max_value=1.000, step=0.001, format="%.3f")
    Fshade = st.number_input("Shading Factor (Fshade)", value=0.950, min_value=0.800, max_value=1.000, step=0.001, format="%.3f")

st.markdown("---")

# ------------ CALCULATIONS SECTION ------------

irr_total = irr_front + irr_rear

# Convert gamma from % to decimal
gP = gammaP / 100
gVoc = gammaVoc / 100
gIsc = gammaIsc / 100

# Temperature adjustments
P_temp = Pmax_stc * (1 + gP * (Tcell - 25))
Voc_temp = Voc_stc * (1 + gVoc * (Tcell - 25))
Isc_temp = Isc_stc * (irr_total / 1000) * (1 + gIsc * (Tcell - 25))

# Correction factors
factor_total = Fmm * Fage * Fg * Fclean * Fshade

# Final outputs
Pout = P_temp * (irr_total / 1000) * factor_total
Vmp = 0.80 * Voc_temp
Imp = 0.92 * Isc_temp

# ------------ DISPLAY SECTION ------------
if st.button("Calculate Parameters"):
    st.success(f"Power Output (Pout): **{Pout:.2f} W**")
    st.info(f"Open Circuit Voltage (Voc): **{Voc_temp:.2f} V**")
    st.info(f"Short Circuit Current (Isc): **{Isc_temp:.2f} A**")
    st.info(f"Voltage at Max Power (Vmp): **{Vmp:.2f} V**")
    st.info(f"Current at Max Power (Imp): **{Imp:.2f} A**")

    # Store in session
    st.session_state["Pout"] = Pout
    st.session_state["Voc"] = Voc_temp
    st.session_state["Isc"] = Isc_temp
    st.session_state["Vmp"] = Vmp
    st.session_state["Imp"] = Imp

