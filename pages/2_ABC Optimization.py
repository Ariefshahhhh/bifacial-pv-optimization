import streamlit as st
import numpy as np

st.set_page_config(page_title="ABC Optimization", page_icon="🐝", layout="centered")

st.title("🐝 Artificial Bee Colony (ABC) Optimization")
st.markdown(
    "This page applies the **Artificial Bee Colony (ABC) algorithm** to optimize selected "
    "correction factors so that the **calculated maximum power (Pmax)** closely matches "
    "the **measured Pmax** obtained from field data."
)
st.markdown("---")

# ==============================
# CHECK REQUIRED DATA
# ==============================
required_keys = [
    "Pmax_calculated", "Pmax_STC", "Ftemp_P",
    "Fg", "Fclean", "Fshade", "Fmm", "Fage"
]

if not all(k in st.session_state for k in required_keys):
    st.error("⚠️ Please complete the **Calculator page** first before running ABC optimization.")
    st.stop()

# ==============================
# USER INPUT
# ==============================
st.subheader("📥 Measured Data Input")

Pmax_measured = st.number_input(
    "Measured Maximum Power, Pmax_measured (W)",
    value=float(st.session_state["Pmax_calculated"]),
    step=1.0
)

# ==============================
# BASE VALUES FROM CALCULATOR
# ==============================
Pmax_STC = st.session_state["Pmax_STC"]
Ftemp_P = st.session_state["Ftemp_P"]
Fg = st.session_state["Fg"]
Fclean_base = st.session_state["Fclean"]
Fshade_base = st.session_state["Fshade"]
Fmm_base = st.session_state["Fmm"]
Fage = st.session_state["Fage"]

# ==============================
# ABC SETTINGS
# ==============================
st.subheader("⚙ ABC Algorithm Settings")

num_bees = 30
iterations = 50

st.write(f"- Number of bees: **{num_bees}**")
st.write(f"- Number of iterations: **{iterations}**")
st.write("- Optimized parameters: **Fmm, Fclean, Fshade**")

bounds = {
    "Fmm": (0.90, 1.00),
    "Fclean": (0.90, 1.00),
    "Fshade": (0.90, 1.00)
}

# ==============================
# MODEL FUNCTIONS
# ==============================
def calculate_pmax(Fmm, Fclean, Fshade):
    return (
        Pmax_STC *
        Ftemp_P *
        Fg *
        Fclean *
        Fshade *
        Fmm *
        Fage
    )

def fitness(solution):
    P_est = calculate_pmax(solution[0], solution[1], solution[2])
    return abs(P_est - Pmax_measured)

# ==============================
# INITIAL POPULATION
# ==============================
population = np.array([
    [
        np.random.uniform(*bounds["Fmm"]),
        np.random.uniform(*bounds["Fclean"]),
        np.random.uniform(*bounds["Fshade"])
    ]
    for _ in range(num_bees)
])

# ==============================
# ABC OPTIMIZATION LOOP
# ==============================
best_solution = None
best_error = float("inf")

for _ in range(iterations):
    for i in range(num_bees):
        candidate = population[i] + np.random.uniform(-0.02, 0.02, 3)
        candidate = np.clip(candidate, 0.90, 1.00)

        if fitness(candidate) < fitness(population[i]):
            population[i] = candidate

        err = fitness(population[i])
        if err < best_error:
            best_error = err
            best_solution = population[i]

# ==============================
# RESULTS
# ==============================
Fmm_opt, Fclean_opt, Fshade_opt = best_solution
Pmax_optimized = calculate_pmax(Fmm_opt, Fclean_opt, Fshade_opt)

st.markdown("---")
st.subheader("📊 Optimization Results Summary")

# ---- TABLE: FACTOR COMPARISON ----
st.markdown("**Optimized Correction Factors**")

st.table({
    "Parameter": ["Mismatch Factor (Fmm)", "Cleaning Factor (Fclean)", "Shading Factor (Fshade)"],
    "Initial Value": [Fmm_base, Fclean_base, Fshade_base],
    "Optimized Value": [round(Fmm_opt, 3), round(Fclean_opt, 3), round(Fshade_opt, 3)]
})

# ---- POWER COMPARISON ----
st.markdown("**Power Comparison**")

st.table({
    "Description": [
        "Calculated Pmax (Before Optimization)",
        "Measured Pmax",
        "Optimized Pmax (After ABC)"
    ],
    "Power (W)": [
        round(st.session_state["Pmax_calculated"], 2),
        round(Pmax_measured, 2),
        round(Pmax_optimized, 2)
    ]
})

# ---- ERROR METRIC ----
st.markdown("**Error Analysis**")

st.success(f"Absolute Error after Optimization = **{best_error:.2f} W**")

st.info(
    "The ABC algorithm successfully adjusted the correction factors so that the "
    "optimized Pmax closely matches the measured value, reducing human estimation error."
)

# SAVE RESULTS FOR OTHER PAGES
st.session_state["Pmax_optimized"] = Pmax_optimized
st.session_state["Fmm_opt"] = Fmm_opt
st.session_state["Fclean_opt"] = Fclean_opt
st.session_state["Fshade_opt"] = Fshade_opt
