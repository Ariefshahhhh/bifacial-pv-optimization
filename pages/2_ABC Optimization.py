import streamlit as st
import numpy as np

st.title("🐝 Artificial Bee Colony (ABC) Optimization")
st.markdown(
    "This module optimizes selected loss factors to minimize the error between "
    "**calculated electrical outputs** and **measured module data**."
)
st.markdown("---")

# ------------------ SAFETY CHECK ------------------
required_keys = [
    "Pmax_calc", "Isc_calc", "Voc_calc", "Vmp_calc", "Imp_calc",
    "Pmax_STC", "Isc_STC", "Voc_STC", "Vmp_STC", "Imp_STC",
    "Ftemp_I", "Ftemp_V", "Ftemp_P", "Fg", "Fage"
]

if not all(k in st.session_state for k in required_keys):
    st.error("❌ Please complete the **Calculator page** first.")
    st.stop()

# ------------------ LOAD DATA ------------------
Pmax_calc = st.session_state["Pmax_calc"]
Isc_calc = st.session_state["Isc_calc"]
Voc_calc = st.session_state["Voc_calc"]
Vmp_calc = st.session_state["Vmp_calc"]
Imp_calc = st.session_state["Imp_calc"]

Pmax_STC = st.session_state["Pmax_STC"]
Isc_STC = st.session_state["Isc_STC"]
Voc_STC = st.session_state["Voc_STC"]
Vmp_STC = st.session_state["Vmp_STC"]
Imp_STC = st.session_state["Imp_STC"]

Ftemp_I = st.session_state["Ftemp_I"]
Ftemp_V = st.session_state["Ftemp_V"]
Ftemp_P = st.session_state["Ftemp_P"]
Fg = st.session_state["Fg"]
Fage = st.session_state["Fage"]

# ------------------ MEASURED INPUT ------------------
st.subheader("📥 Measured Module Data")
col1, col2 = st.columns(2)

with col1:
    Pmax_meas = st.number_input("Measured Pmax (W)", value=Pmax_calc)
    Voc_meas = st.number_input("Measured Voc (V)", value=Voc_calc)

with col2:
    Isc_meas = st.number_input("Measured Isc (A)", value=Isc_calc)
    Vmp_meas = st.number_input("Measured Vmp (V)", value=Vmp_calc)

# ------------------ ABC PARAMETERS ------------------
st.markdown("---")
st.subheader("⚙ ABC Parameters")

iters = st.slider("Iterations", 50, 300, 150, step=10)
bees = st.slider("Number of Bees", 10, 50, 25, step=5)

# ------------------ ABC FUNCTIONS ------------------
def calculate_outputs(Fclean, Fshade, Fmm):
    Isc = Isc_STC * Ftemp_I * Fg * Fclean * Fshade
    Voc = Voc_STC * Ftemp_V
    Vmp = Vmp_STC * Ftemp_V
    Imp = Imp_STC * Ftemp_I * Fg * Fclean * Fshade
    Pmax = Pmax_STC * Ftemp_P * Fg * Fclean * Fshade * Fmm * Fage
    return Pmax, Isc, Voc, Vmp, Imp

def error_function(sol):
    Fclean, Fshade, Fmm = sol
    Pmax, Isc, Voc, Vmp, _ = calculate_outputs(Fclean, Fshade, Fmm)

    return (
        abs(Pmax - Pmax_meas) +
        abs(Isc - Isc_meas) +
        abs(Voc - Voc_meas) +
        abs(Vmp - Vmp_meas)
    )

def run_abc():
    colony = np.random.uniform(0.85, 1.0, (bees, 3))
    best = None
    best_err = float("inf")

    history = []

    for _ in range(iters):
        for i in range(bees):
            err = error_function(colony[i])
            if err < best_err:
                best_err = err
                best = colony[i].copy()

            colony[i] += np.random.uniform(-0.01, 0.01, 3)
            colony[i] = np.clip(colony[i], 0.85, 1.0)

        history.append(best_err)

    return best, best_err, history

# ------------------ RUN ABC ------------------
if st.button("🚀 Run ABC Optimization"):
    best_sol, best_err, history = run_abc()
    Fclean_opt, Fshade_opt, Fmm_opt = best_sol

    Pmax_opt, Isc_opt, Voc_opt, Vmp_opt, Imp_opt = calculate_outputs(
        Fclean_opt, Fshade_opt, Fmm_opt
    )

    # Save optimized values
    st.session_state["Pmax_opt"] = Pmax_opt
    st.session_state["Isc_opt"] = Isc_opt
    st.session_state["Voc_opt"] = Voc_opt
    st.session_state["Vmp_opt"] = Vmp_opt
    st.session_state["Imp_opt"] = Imp_opt

    # ------------------ RESULTS ------------------
    st.markdown("---")
    st.subheader("📊 Optimized Results Summary")

    colA, colB, colC = st.columns(3)

    with colA:
        st.metric("Optimized Pmax (W)", f"{Pmax_opt:.2f}", f"{Pmax_opt - Pmax_meas:.2f}")

    with colB:
        st.metric("Optimized Isc (A)", f"{Isc_opt:.3f}", f"{Isc_opt - Isc_meas:.3f}")

    with colC:
        st.metric("Optimized Voc (V)", f"{Voc_opt:.2f}", f"{Voc_opt - Voc_meas:.2f}")

    colD, colE = st.columns(2)
    with colD:
        st.metric("Optimized Vmp (V)", f"{Vmp_opt:.2f}", f"{Vmp_opt - Vmp_meas:.2f}")
    with colE:
        st.metric("Optimized Imp (A)", f"{Imp_opt:.3f}")

    # ------------------ FACTORS ------------------
    st.markdown("---")
    st.subheader("⚙ Optimized Loss Factors")

    st.success(f"**Fclean (Cleaning Factor)** = {Fclean_opt:.3f}")
    st.success(f"**Fshade (Shading Factor)** = {Fshade_opt:.3f}")
    st.success(f"**Fmm (Mismatch Factor)** = {Fmm_opt:.3f}")

    st.info(f"Total Optimization Error = **{best_err:.3f}**")
