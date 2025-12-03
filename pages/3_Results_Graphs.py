import streamlit as st
import matplotlib.pyplot as plt

st.title("📊 Results & Visual Analysis")
st.markdown("---")

if "P_optimized" not in st.session_state:
    st.warning("⚠️ No optimization results available. Run ABC Optimization first.")
    st.stop()

P_measured = st.session_state["P_measured"]
Pout = st.session_state["P_calculated"]
P_opt = st.session_state["P_optimized"]
err_before = st.session_state["error_before"]
err_after = st.session_state["error_after"]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Measured Power", f"{P_measured:.2f} W")

with col2:
    st.metric("Calculated Power", f"{Pout:.2f} W", delta=f"{Pout - P_measured:.2f}")

with col3:
    st.metric("Optimized Power", f"{P_opt:.2f} W", delta=f"{P_opt - P_measured:.2f}")

st.markdown("### 🔍 Power Comparison Chart")

fig, ax = plt.subplots()
ax.bar(["Measured", "Calculated", "Optimized"], [P_measured, Pout, P_opt])
ax.set_ylabel("Power (W)")
ax.set_title("Measured vs Calculated vs Optimized")
ax.grid(axis="y", linestyle="--")
st.pyplot(fig)

st.markdown("### 📉 Error Before vs After Optimization")

fig2, ax2 = plt.subplots()
ax2.bar(["Before", "After"], [err_before, err_after])
ax2.set_ylabel("Absolute Error (W)")
ax2.set_title("Error Reduction")
ax2.grid(axis="y", linestyle="--")
st.pyplot(fig2)
