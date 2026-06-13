import numpy as np
import chart_studio.plotly as py
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import sympy as smp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

st.set_page_config(page_title="Calculator", layout="wide")

transformations = (
    standard_transformations +
    (implicit_multiplication_application,) +
    (convert_xor,)
)

column1, column2 = st.columns([4,5])

x, a, b, y, z=smp.symbols("x, a, b, y, z")

sidebar = st.sidebar

with sidebar:
    selected = st.selectbox("Select a tool:", ["integral", "equation", "derivative", "definite integral", "limit", "double integral"])
    if selected == "definite integral":
        st.divider()
        upper_bound=st.number_input("Insert the upper bound", value=0)
        lower_bound=st.number_input("Insert the lower bound", value=0)
    if selected == "limit":
        st.divider()
        limit_val = st.text_input("", value=0)
        limit = st.radio("Limit as x→", [limit_val, "∞", "-∞"])
        try:
            limit_num = float(smp.parse_expr(limit_val, transformations=transformations, local_dict={"e": smp.E}))
        except:
            st.error("Please enter an integer or a mathematical value eg. pi/2")
    if selected == "double integral":
        order = st.radio("Select the order of integration", ["dxdy","dydx"])
        c1,c2 = st.columns([1,1])
        with c1: 
            x_low=st.text_input("Insert the x lower bound", value=0)
            x_up=st.text_input("Insert the x upper bound", value=0)
        with c2:
            y_low=st.text_input("Insert the y lower bound", value=0)
            y_up=st.text_input("Insert the y upper bound", value=0)

with column1: 
    c1, c2 = st.columns([2,1])
    with c1:
        st.header("Calculator")
        st.divider()
        if selected == "equation": 
            equatio=st.text_input("Write the equation", value="5+5")
            try:
                equation = smp.parse_expr(equatio, transformations=transformations, local_dict={"e": smp.E})
            except:
                pass
        elif selected == "double integral":
            equatio = st.text_input("f(x,y)=", value="x")
            try:
                equation = smp.parse_expr(equatio, transformations=transformations, local_dict={"e": smp.E})
            except:
                pass
        else: 
            equatio = st.text_input("f(x,y)=", value="x")
            try:
                equation = smp.parse_expr(equatio, transformations=transformations, local_dict={"e": smp.E})
            except:
                pass
with column2:
    st.header("Answer")
    st.divider()
    c1,c2,c3 = st.columns([1,1,1])
    with st.container(border=True):
        if selected == "equation":
            try:
                if equation.free_symbols:
                    st.error("Enter a number/expression, not a function")
                else:
                    with c1: 
                        st.write(equation)
                    with c2:
                        st.write("")
                        st.write("or")
                    with c3:
                        st.write("")
                        st.text(float(equation))
            except:
                st.error("Invalid expression")
        if selected == "integral":
            st.latex(smp.integrate(equation, x))
        if selected =="definite integral":
            c1,c2,c3 = st.columns([1,1,1])
            with c1:
                try:
                    Integral=(smp.integrate(equation, (x, lower_bound, upper_bound)))
                    st.latex(Integral)
                except:
                    pass
            with c2:
                st.write("")
                st.write("or")
            with c3:
                try:
                    st.write("")
                    st.metric(label="Numeric result:", value=float(Integral))
                except: st.warning("Couldn't convert to float")
        if selected == "derivative":
            try:
                st.latex(smp.diff(equation))
            except:
                pass
        if selected == "limit":
            try:
                if limit == limit_val:
                    st.latex(smp.limit(equation, x, limit_num))
                elif limit == "∞":
                    st.latex(smp.limit(equation, x, smp.oo))
                elif limit=="-∞":
                    st.latex(smp.limit(equation, x, -smp.oo))
            except:
                st.error("Could not compute, please check function and approach value")
        if selected == "double integral":
            try:
                if x_low and x_up and y_low and y_up:
                    xlow = smp.parse_expr(x_low, transformations=transformations, local_dict={"e": smp.E})
                    xup = smp.parse_expr(x_up, transformations=transformations, local_dict={"e": smp.E})
                    ylow = smp.parse_expr(y_low, transformations=transformations, local_dict={"e": smp.E})
                    yup = smp.parse_expr(y_up, transformations=transformations, local_dict={"e": smp.E})
                    if order == "dydx":
                        st.latex(smp.integrate(equation, (y, ylow, yup), (x, xlow, xup)))
                    else:
                        st.latex(smp.integrate(equation, (x, xlow, xup), (y, ylow, yup)))
            except Exception as e:
                st.warning("Could not compute the double integral, use a and b if you need constants in the bounds")

fig=go.Figure()
x_val=np.linspace(-1000,1000,100000)
try:
    if smp.diff(equation) == 0:
        f=smp.lambdify(x, equation, "numpy")
        y_val = np.array([f(val) for val in x_val])
    else:
        f=smp.lambdify(x, equation, "numpy")
        y_val=f(x_val)
        dy=np.abs(np.diff(y_val))
        y_val[:-1][dy > 100] = np.nan
    fig.add_trace(go.Scatter(x=x_val, y=y_val, mode="lines", name=equatio,
    line=dict(color="#0091f9", width=4)))
    fig.update_layout(
    hovermode="x unified",
    template="plotly_white", 
    xaxis=dict(
        range=[-5, 5],
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(200,200,200,0.7)",
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor="black"
    ),
    yaxis=dict(
        range=[-5, 5],
        showgrid=True,
        gridwidth=1,
    gridcolor="rgba(200,200,200,0.7)",
    zeroline=True,
    zerolinewidth=2,
    zerolinecolor="black"
    ),
    plot_bgcolor="white",
    height=800,
    )
    if(selected=="definite integral"):
        fig.add_trace(go.Scatter(
            x=x_val[(x_val >= lower_bound) & (x_val <= upper_bound)],
            y=y_val[(x_val >= lower_bound) & (x_val <= upper_bound)],
            fill="tozeroy", fillcolor="rgba(99, 110, 250, 0.3)",
            line=dict(color="rgba(0,0,0,0)"), name="integral area"
))
    st.plotly_chart(fig)
except Exception as e: 
    st.warning(f"Could not plot '{equation}'")
    st.write(e)

