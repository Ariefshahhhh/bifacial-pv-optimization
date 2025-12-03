import streamlit as st
import numpy as np

st.title("🐝 ABC Optimization")
st.markdown("Optimize correction factors to minimize the error between calculated and measured power.")
st.markdown("---")

# Get values from calculator
if "P_calculated" not in st.session_state:
    st.warning("⚠️ No baseline calculation found. Please use the PV Calculator first.")
    st.stop()

Pout = st.session_state["P_calculated"]
irr_total = st.session_state["irr_total"]
temp_factor = st.session_state["temp_factor"]
Pmax_stc = st.session_state["Pmax_stc"]

# User input (Measured)
P_measured = st.number_input("Measured Output Power (W)", value=350.0)

def calc_power(Pmax, irr, tf, fac):
    Fmm, Fclean, Fshade = fac
    return Pmax * (irr/1000) * tf * Fmm * Fclean * Fshade

def objective(fac, Pmax, irr, tf, Pm):
    return abs(calc_power(Pmax, irr, tf, fac) - Pm)

def ABC(Pmax, irr, tf, Pm, iters=200, size=30):
    sols = np.random.uniform(0.8, 1.0, (size, 3))
    best = None
    best_err = 999

    for _ in range(iters):
        for i in range(size):
            err = objective(sols[i], Pmax, irr, tf, Pm)
            if err < best_err:
                best_err = err
                best = sols[i].copy()

            sols[i] += np.random.uniform(-0.01, 0.01, 3)
            sols[i] = np.clip(sols[i], 0.8, 1.0)

    return best, best_err

if st.button("Run ABC Optimization"):
    best_factors, best_err = ABC(Pmax_stc, irr_total, temp_factor, P_measured)

    P_opt = calc_power(Pmax_stc, irr_total, temp_factor, best_factors)

    st.success(f"Optimized Output Power: **{P_opt:.2f} W**")
    st.info(f"Minimized Error: **{best_err:.3f} W**")

    st.session_state["P_measured"] = P_measured
    st.session_state["P_optimized"] = P_opt
    st.session_state["error_after"] = best_err
    st.session_state["error_before"] = abs(Pout - P_measured)

    st.session_state["best_factors"] = best_factors

    st.success("Optimization complete! Go to **Results & Graphs** page.")

