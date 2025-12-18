import streamlit as st
import numpy as np

st.title("🐝 Artificial Bee Colony (ABC) Optimization")
st.markdown(
    "This page optimizes selected correction factors using the Artificial Bee Colony (ABC) algorithm "
    "to minimize the error between **calculated** and **measured** maximum power (Pmax)."
)
st.markdown("---")

# -------------------------------------------------
# CHECK REQUIRED DATA FROM CALCULATOR PAGE
# -------------------------------------------------
required_keys = [
    "Pmax_calculated", "Pmax_STC", "Ftemp_P",
    "Fg", "Fclean", "Fshade", "Fmm", "Fage"
]

if not all(k in st.session_state for k in required_keys):
    st.error("⚠️ Please complete the **Calculator page** first.")
    st.stop()

# -------------------------------------------------
# USER INPUT
# -------------------------------------------------
st.subheader("📥 Measured Data Input")

Pmax_measured = st.number_input(
    "Measured Maximum Power, Pmax_measured (W)",
    value=float(st.session_state["Pmax_calculated"]),
    step=1.0,
    help="Measured output power obtained from field measurement or instrument."
)

# -------------------------------------------------
# RETRIEVE BASE VALUES
# -------------------------------------------------
Pmax_STC = st.session_state["Pmax_STC"]
Ftemp_P = st.session_state["Ftemp_P"]
Fg = st.session_state["Fg"]
Fclean = st.session_state["Fclean"]
Fshade = st.session_state["Fshade"]
Fmm_base = st.session_state["Fmm"]
Fage_base = st.session_state["Fage"]

# -------------------------------------------------
# ABC PARAMETERS
# -------------------------------------------------
st.subheader("⚙ ABC Algorithm Parameters")

num_bees = st.slider("Number of Bees", 10, 60, 30)
iterations = st.slider("Number of Iterations", 20, 200, 50)

# Optimize selected factors (Option A)
bounds = {
    "Fmm": (0.90, 1.00),
    "Fclean": (0.90, 1.00),
    "Fshade": (0.90, 1.00)
}

# -------------------------------------------------
# MODEL FUNCTIONS
# -------------------------------------------------
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
    P_est = calculate_pmax(solution[0], solution[1], solution[2])
    return abs(P_est - Pmax_measured)

# -------------------------------------------------
# RUN ABC BUTTON
# -------------------------------------------------
st.markdown("---")
run_abc = st.button("🐝 Run ABC Optimization")

if run_abc:

    # -------- INITIAL POPULATION --------
    population = np.array([
        [
            np.random.uniform(*bounds["Fmm"]),
            np.random.uniform(*bounds["Fclean"]),
            np.random.uniform(*bounds["Fshade"])
        ]
        for _ in range(num_bees)
    ])

    best_solution = population[0]
    best_error = fitness(best_solution)

    # -------- ABC MAIN LOOP --------
    for _ in range(iterations):
        for i in range(num_bees):

            candidate = population[i] + np.random.uniform(-0.02, 0.02, 3)
            candidate = np.clip(candidate, 0.9, 1.0)

            if fitness(candidate) < fitness(population[i]):
                population[i] = candidate

            current_error = fitness(population[i])
            if current_error < best_error:
                best_error = current_error
                best_solution = population[i]

    # -------- RESULTS --------
    Fmm_opt, Fclean_opt, Fshade_opt = best_solution
    Pmax_optimized = calculate_pmax(Fmm_opt, Fclean_opt, Fshade_opt)

    st.markdown("---")
    st.subheader("✅ Optimization Results")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**🔧 Optimized Correction Factors**")
        st.success(f"Mismatch Factor, Fmm = {Fmm_opt:.3f}")
        st.success(f"Cleaning Factor, Fclean = {Fclean_opt:.3f}")
        st.success(f"Shading Factor, Fshade = {Fshade_opt:.3f}")

    with col2:
        st.markdown("**⚡ Power Comparison**")
        st.info(f"Calculated Pmax (Before ABC) = {st.session_state['Pmax_calculated']:.2f} W")
        st.info(f"Optimized Pmax (After ABC) = {Pmax_optimized:.2f} W")
        st.info(f"Measured Pmax = {Pmax_measured:.2f} W")

    st.markdown("**📉 Optimization Accuracy**")
    st.warning(f"Absolute Error after Optimization = {best_error:.2f} W")

    st.markdown(
        "> **Note:** The ABC algorithm iteratively adjusts the selected correction factors "
        "to minimize the difference between calculated and measured Pmax, improving model accuracy."
    )
