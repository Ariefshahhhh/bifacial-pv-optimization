import streamlit as st
import numpy as np

st.title("🐝 Artificial Bee Colony (ABC) Optimization")
st.markdown("Optimize correction factors to minimize error between calculated and measured Pmax.")
st.markdown("---")

# ---- CHECK REQUIRED DATA ----
required_keys = [
    "Pmax_calculated", "Pmax_STC", "Ftemp_P",
    "Fg", "Fclean", "Fshade", "Fmm", "Fage"
]

if not all(k in st.session_state for k in required_keys):
    st.error("⚠️ Please complete the Calculator page first.")
    st.stop()

# ---- USER INPUT ----
Pmax_measured = st.number_input(
    "Measured Pmax (W)",
    value=st.session_state["Pmax_calculated"],
    step=1.0
)

# ---- BASE VALUES ----
Pmax_STC = st.session_state["Pmax_STC"]
Ftemp_P = st.session_state["Ftemp_P"]
Fg = st.session_state["Fg"]
Fclean = st.session_state["Fclean"]
Fshade = st.session_state["Fshade"]
Fmm_base = st.session_state["Fmm"]
Fage_base = st.session_state["Fage"]

# ---- ABC SETTINGS ----
num_bees = 30
iterations = 50

# Optimize only selected factors (Option A)
bounds = {
    "Fmm": (0.90, 1.00),
    "Fclean": (0.90, 1.00),
    "Fshade": (0.90, 1.00)
}

def calculate_pmax(Fmm, Fclean, Fshade):
    return (
        Pmax_STC *
        Ftemp_P *
        Fg *
        Fclean *
        Fshade *
        Fmm *
        Fage_base
    )

def fitness(solution):
    P_est = calculate_pmax(
        solution[0], solution[1], solution[2]
    )
    return abs(P_est - Pmax_measured)

# ---- INITIAL POPULATION ----
population = np.array([
    [
        np.random.uniform(*bounds["Fmm"]),
        np.random.uniform(*bounds["Fclean"]),
        np.random.uniform(*bounds["Fshade"])
    ]
    for _ in range(num_bees)
])

# ---- ABC LOOP ----
best_solution = None
best_error = float("inf")

for _ in range(iterations):
    for i in range(num_bees):
        candidate = population[i] + np.random.uniform(-0.02, 0.02, 3)
        candidate = np.clip(candidate, 0.9, 1.0)

        if fitness(candidate) < fitness(population[i]):
            population[i] = candidate

        err = fitness(population[i])
        if err < best_error:
            best_error = err
            best_solution = population[i]

# ---- RESULTS ----
Fmm_opt, Fclean_opt, Fshade_opt = best_solution
Pmax_optimized = calculate_pmax(Fmm_opt, Fclean_opt, Fshade_opt)

st.markdown("---")
st.subheader("✅ Optimization Results")

st.success(f"Optimized Fmm = {Fmm_opt:.3f}")
st.success(f"Optimized Fclean = {Fclean_opt:.3f}")
st.success(f"Optimized Fshade = {Fshade_opt:.3f}")

st.info(f"Optimized Pmax = {Pmax_optimized:.2f} W")
st.info(f"Measured Pmax = {Pmax_measured:.2f} W")
st.warning(f"Absolute Error = {best_error:.2f} W")
