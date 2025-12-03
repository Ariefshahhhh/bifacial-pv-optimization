import streamlit as st

st.title("⚡ PV Output Power Computation Tool")
st.markdown("Calculate bifacial PV power output with complete correction factors.")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    Pmax_stc = st.number_input("Module Pmax at STC (W)", value=450.0)
    irr_front = st.number_input("Front Irradiance (W/m²)", value=800.0)
    irr_rear = st.number_input("Rear Irradiance (W/m²)", value=100.0)
    temp_coeff = st.number_input("Temperature Coefficient γ (per °C)", value=0.004)
    Tcell = st.number_input("Cell Temperature (°C)", value=30.0)

with col2:
    Fmm = st.number_input("Mismatch Factor (Fmm)", value=0.98, min_value=0.80, max_value=1.00, step=0.01)
    Fdegrad = st.number_input("Degradation Factor (Fdegrad)", value=0.99, min_value=0.80, max_value=1.00, step=0.01)
    Fg = st.number_input("Glass/Soiling Factor (Fg)", value=0.97, min_value=0.80, max_value=1.00, step=0.01)
    Fclean = st.number_input("Cleaning Factor (Fclean)", value=0.98, min_value=0.80, max_value=1.00, step=0.01)
    Funshade = st.number_input("Unshaded Factor (Funshade)", value=0.95, min_value=0.80, max_value=1.00, step=0.01)

irr_total = irr_front + irr_rear
temp_factor = 1 - temp_coeff * (Tcell - 25)

Pout = (
    Pmax_stc *
    (irr_total / 1000) *
    temp_factor *
    Fmm *
    Fdegrad *
    Fg *
    Fclean *
    Funshade
)

st.markdown("---")
if st.button("Calculate Output Power"):
    st.success(f"Calculated Output Power = **{Pout:.2f} W**")

    # Save values for optimization page
    st.session_state["P_calculated"] = Pout
    st.session_state["irr_total"] = irr_total
    st.session_state["temp_factor"] = temp_factor
    st.session_state["Pmax_stc"] = Pmax_stc

