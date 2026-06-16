import streamlit as st

st.set_page_config(page_title="Axis", layout="wide")

st.title("Axis")
st.write("Built with Python, SymPy, NumPy and Plotly. Pick a tool from the sidebar or click a card below.")
st.divider()

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("Graphing calculator")
        st.write("Plot multiple functions simultaneously. Compute derivatives, zeros, average value, and arc length.")
        st.code("try: sin(x)/x", language=None)
        st.page_link("pages/01_Graphing_Calculator.py", label="Open →")

    with st.container(border=True):
        st.subheader("Calculator")
        st.write("Symbolic computation: integrals, derivatives, limits, and double/triple integrals with exact results.")
        st.code("try: ∫ sin(x²) dx", language=None)
        st.page_link("pages/02_Calculator.py", label="Open →")

with col2:
    with st.container(border=True):
        st.subheader("3D plotter")
        st.write("Visualize surfaces f(x, y) in 3D. Finds critical points, saddle points, and partial derivatives.")
        st.code("try: sin(x)*cos(y)", language=None)
        st.page_link("pages/03_3D_Plotter.py", label="Open →")

    with st.container(border=True):
        st.subheader("Vector fields")
        st.write("Visualize 2D vector fields. Computes curl, divergence, work integrals, and flux integrals.")
        st.code("try: U = -y, V = x ", language=None)
        st.page_link("pages/04_Vector_Fields.py", label="Open →")

st.divider()
st.caption("Built for Hack Club Stardance 2026")