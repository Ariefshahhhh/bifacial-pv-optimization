import streamlit as st
import numpy as np

st.title("🐝 Artificial Bee Colony (ABC) Optimization")
st.markdown("Optimize correction factors to minimize error between calculated and measured Pmax.")
st.markdown("---")

# --------- SAFETY CHECK ----------
required_keys = [
    "Pmax_STC", "Ftemp_P", "Fg", "Fage",
    "Pmax_calculated"
]

if not all(k in st.session_state for k in required_keys):
    st.error("⚠️ Please complete the Calculator page first.")
    st.stop()

# --------- GET VALUES FROM CALCULATOR ----------
Pmax_STC = st.session_state["Pmax_STC"]
Ftemp_P = st.session_state["Ftemp_P"]
Fg = st.session_state["Fg"]
Fage = st.session_state["Fage"]
P_calc_initial = st.session_state["Pmax_calculated"]

# --------- USER INPUT ----------
P_measured = st.number_input(
    "Measured Maximum Power (Pmax_measured) [W]",
    value=float(P_calc_initial),
    step=1.0
)

st.markdown("---")

# --------- ABC PARAMETERS ----------
num_bees = st.slider("Number of Bees", 10, 50, 20)
iterations = st.slider("Iterations", 50, 300, 150)

# --------- SEARCH BOUNDS ----------
bounds = {
    "Fclean": (0.85, 1.00),
    "Fshade": (0.80, 1.00),
    "Fmm": (0.90, 1.00),
}

# --------- OBJECTIVE FUNCTION ----------
def calculate_pmax(factors):
    Fclean, Fshade, Fmm = factors
    return (
        Pmax_STC *
        Ftemp_P *
        Fg *
        Fclean *
        Fshade *
        Fmm *
        Fage
    )

def objective(factors):
    return abs(calculate_pmax(factors) - P_measured)

# --------- ABC CORE ----------
def run_abc():
    solutions = np.random.uniform(
        [bounds[k][0] for k in bounds],
        [bounds[k][1] for k in bounds],
        (num_bees, 3)
    )

    best_solution = None
    best_error = float("inf")

    for _ in range(iterations):
        for i in range(num_bees):
            candidate = solutions[i] + np.random.uniform(-0.02, 0.02, 3)
            candidate = np.clip(
                candidate,
                [bounds[k][0] for k in bounds],
                [bounds[k][1] for k in bounds]
            )

            err = objective(candidate)

            if err < best_error:
                best_error = err
                best_solution = candidate

    return best_solution, best_error

# --------- RUN BUTTON ----------
if st.button("Run ABC Optimization"):
    best_factors, best_error = run_abc()

    Fclean_opt, Fshade_opt, Fmm_opt = best_factors
    Pmax_opt = calculate_pmax(best_factors)

    st.markdown("### ✅ Optimized Results")

    st.success(f"Optimized Fclean = {Fclean_opt:.3f}")
    st.success(f"Optimized Fshade = {Fshade_opt:.3f}")
    st.success(f"Optimized Fmm = {Fmm_opt:.3f}")

    st.markdown("---")

    st.metric("Calculated Pmax (Before ABC)", f"{P_calc_initial:.2f} W")
    st.metric("Optimized Pmax (After ABC)", f"{Pmax_opt:.2f} W")
    st.metric("Measured Pmax", f"{P_measured:.2f} W")
    st.metric("Final Absolute Error", f"{best_error:.3f} W")

    # --------- SAVE RESULTS ----------
    st.session_state["Pmax_optimized"] = Pmax_opt
    st.session_state["Fclean_opt"] = Fclean_opt
    st.session_state["Fshade_opt"] = Fshade_opt
    st.session_state["Fmm_opt"] = Fmm_opt
