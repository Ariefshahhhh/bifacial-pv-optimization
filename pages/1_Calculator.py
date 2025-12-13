import streamlit as st

st.title("⚡ Bifacial PV Output Computation Tool")
st.markdown(
    "Compute **Output Power**, **Voltage at Maximum Power**, "
    "**Current at Maximum Power**, **Open-Circuit Voltage**, "
    "and **Short-Circuit Current** with temperature correction and loss factors."
)
st.markdown("---")

# ================= LAYOUT =================
col1, col2 = st.columns(2)

# ---------- LEFT SIDE ----------
with col1:
    st.subheader("🔆 Environmental Inputs")

    G_front = st.number_input("Front Irradiance (W/m²)", value=800.0)
    G_rear = st.number_input("Rear Irradiance (W/m²)", value=100.0)
    Tcell = st.number_input("Cell Temperature (°C)", value=30.0)

    st.subheader("📦 Module STC Electrical Data")
    Pmax_stc = st.number_input("Maximum Power at STC (W)", value=450.0)
    Vmp_stc = st.number_input("Voltage at Maximum Power at STC (V)", value=41.0, step=0.1)
    Imp_stc = st.number_input("Current at Maximum Power at STC (A)", value=10.98, step=0.01)
    Voc_stc = st.number_input("Open-Circuit Voltage at STC (V)", value=49.5, step=0.1)
    Isc_stc = st.number_input("Short-Circuit Current at STC (A)", value=11.50, step=0.01)

# ---------- RIGHT SIDE ----------
with col2:
    st.subheader("🌡 Temperature Coefficients")

    alpha = st.number_input(
        "α (Short-Circuit Current Temperature Coefficient, 1/°C)",
        value=0.040, format="%.3f"
    )
    beta = st.number_input(
        "β (Voltage Temperature Coefficient, 1/°C)",
        value=-0.280, format="%.3f"
    )
    gamma = st.number_input(
        "γ (Maximum Power Temperature Coefficient, 1/°C)",
        value=-0.350, format="%.3f"
    )

    st.subheader("⚙ Correction Factors")
    Fmm = st.number_input("Mismatch Factor (Fmm)", value=0.98, min_value=0.80, max_value=1.00, step=0.01)
    Fage = st.number_input("Aging Factor (Fage)", value=0.95, min_value=0.80, max_value=1.00, step=0.01)
    Fg = st.number_input("Glass / Soiling Factor (Fg)", value=0.97, min_value=0.80, max_value=1.00, step=0.01)
    Fclean = st.number_input("Cleaning Factor (Fclean)", value=0.98, min_value=0.80, max_value=1.00, step=0.01)
    Fshade = st.number_input("Shading Factor (Fshade)", value=0.95, min_value=0.80, max_value=1.00, step=0.01)

# ================= CALCULATION =================
if st.button("Calculate Electrical Outputs"):

    G_total = G_front + G_rear

    # ---- Temperature corrections ----
    Short_Circuit_Current = Isc_stc * (1 + alpha * (Tcell - 25))
    Open_Circuit_Voltage = Voc_stc * (1 + beta * (Tcell - 25))
    Maximum_Power_Temp = Pmax_stc * (1 + gamma * (Tcell - 25))

    # ---- Output Power Calculation ----
    Output_Power = (
        Maximum_Power_Temp *
        (G_total / 1000) *
        Fmm *
        Fage *
        Fg *
        Fclean *
        Fshade
    )

    # ---- Voltage & Current at Maximum Power ----
    Voltage_at_Maximum_Power = Vmp_stc * (1 + beta * (Tcell - 25))
    Current_at_Maximum_Power = (
        Output_Power / Voltage_at_Maximum_Power
        if Voltage_at_Maximum_Power != 0 else 0
    )

    # ================= OUTPUT DISPLAY =================
    st.markdown("---")
    st.subheader("📊 Calculated Electrical Outputs")

    colA, colB = st.columns(2)

    with colA:
        st.success(f"**Output Power (Pₒᵤₜ)** = {Output_Power:.2f} W")
        st.success(f"**Voltage at Maximum Power (Vₘₚ)** = {Voltage_at_Maximum_Power:.2f} V")
        st.success(f"**Open-Circuit Voltage (Vₒ𝒸)** = {Open_Circuit_Voltage:.2f} V")

    with colB:
        st.success(f"**Current at Maximum Power (Iₘₚ)** = {Current_at_Maximum_Power:.2f} A")
        st.success(f"**Short-Circuit Current (Iₛ𝒸)** = {Short_Circuit_Current:.2f} A")

    # ================= SAVE FOR ABC =================
    st.session_state["Output_Power"] = Output_Power
    st.session_state["Voltage_at_Maximum_Power"] = Voltage_at_Maximum_Power
    st.session_state["Current_at_Maximum_Power"] = Current_at_Maximum_Power
    st.session_state["Open_Circuit_Voltage"] = Open_Circuit_Voltage
    st.session_state["Short_Circuit_Current"] = Short_Circuit_Current
    st.session_state["G_total"] = G_total
    st.session_state["gamma"] = gamma

    st.info("All calculated values are saved and ready for ABC Optimization.")
