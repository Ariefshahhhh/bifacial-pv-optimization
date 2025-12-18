import streamlit as st
import numpy as np

st.title("🐝 Artificial Bee Colony (ABC) Optimization")
st.markdown(
    "This module optimizes correction factors to **minimize the error between calculated "
    "maximum power and measured maximum power at module level**."
)
st.markdown("---")

# -------------------------------
# CHECK REQUIRED DATA FROM CALCULATOR
# -------------------------------
required_keys = [
    "Pmax_calculated",
    "Pmax_stc",
    "Ftemp_P",
    "Fg",
    "Fclean",
    "Fshade",
    "Fmm",
    "Fage"
]

missing = [k for k in required_keys if k not in st.session_state]

if missing:
    st.error("⚠ Please complete the **Calculator page** first.")
    st.stop()

# -------------------------------
# LOAD DATA FROM SESSION STATE
# -------------------------------
Pcalc = st.session_state["Pmax_calculated"]
Pstc = st.session_state["Pmax_stc"]
Ftemp_P = st.session_state["Ftemp_P"]
Fg = st.session_state["Fg"]
Fclean = st.session_state["Fclean"]
Fshade = st.session_state["Fshade"]
Fmm = st.session_state["Fmm"]
Fage = st.session_state["Fage"]

# -------------------------------
# MEASURED POWER INPUT
# -------------------------------
st.subheader("📏 Measured Reference Data")

P_measured = st.number_input(
    "Measured Maximum Power, Pmax,measured (W)",
    min_value=0.0,
    value=float(Pcalc),
    step=1.0
)

st.markdown("---")

# -------------------------------
# ABC PARAMETERS
# -------------------------------
st.subheader("🐝 ABC Algorithm Settings")

col1, col2 = st.columns(2)
with col1:
    n_bees = st.number_input("Number of Bees", 10, 100, 30)
with col2:
    n_iter = st.number_input("Number of Iterations", 10, 300, 100)

# -------------------------------
# ABC OBJECTIVE FUNCTION
# -------------------------------
def calculate_pmax(Fmm_x, Fclean_x, Fshade_x):
    return (
        Pstc
        * Ftemp_P
        * Fg
        * Fclean_x
        * Fshade_x
        * Fmm_x
        * Fage
    )

def fitness(solution):
    P_est = calculate_pmax(*solution)
    return abs(P_est - P_measured)

# -------------------------------
# RUN ABC
# -------------------------------
if st.button("🚀 Run ABC Optimization"):

    # INITIAL POPULATION
    bees = np.random.uniform(0.90, 1.00, (n_bees, 3))
    fitness_vals = np.array([fitness(b) for b in bees])

    for _ in range(n_iter):
        for i in range(n_bees):
            k = np.random.randint(0, n_bees)
            phi = np.random.uniform(-1, 1, 3)
            candidate = bees[i] + phi * (bees[i] - bees[k])
            candidate = np.clip(candidate, 0.90, 1.00)

            if fitness(candidate) < fitness_vals[i]:
                bees[i] = candidate
                fitness_vals[i] = fitness(candidate)

    best_idx = np.argmin(fitness_vals)
    best_solution = bees[best_idx]

    Fmm_opt, Fclean_opt, Fshade_opt = best_solution
    Popt = calculate_pmax(Fmm_opt, Fclean_opt, Fshade_opt)
    error_opt = abs(Popt - P_measured)

    # -------------------------------
    # DISPLAY RESULTS
    # -------------------------------
    st.markdown("---")
    st.subheader("✅ Optimization Results")

    colA, colB = st.columns(2)

    with colA:
        st.success(f"**Optimized Mismatch Factor (Fmm)** = {Fmm_opt:.4f}")
        st.success(f"**Optimized Cleaning Factor (Fclean)** = {Fclean_opt:.4f}")
        st.success(f"**Optimized Shading Factor (Fshade)** = {Fshade_opt:.4f}")

    with colB:
        st.info(f"**Calculated Pmax (Before ABC)** = {Pcalc:.2f} W")
        st.info(f"**Optimized Pmax (After ABC)** = {Popt:.2f} W")
        st.info(f"**Measured Pmax** = {P_measured:.2f} W")

    st.markdown("---")
    st.subheader("📉 Error Analysis")

    st.metric(
        label="Absolute Error After Optimization (W)",
        value=f"{error_opt:.3f}"
    )

    # -------------------------------
    # SAVE FOR RESULTS PAGE
    # -------------------------------
    st.session_state["Pmax_optimized"] = Popt
    st.session_state["ABC_Fmm"] = Fmm_opt
    st.session_state["ABC_Fclean"] = Fclean_opt
    st.session_state["ABC_Fshade"] = Fshade_opt
    st.session_state["ABC_error"] = error_opt

    st.success("✅ Optimized values saved. Proceed to **Results & Graphs** page.")
