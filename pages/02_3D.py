import numpy as np
import chart_studio.plotly as py
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import sympy as smp

st.set_page_config(page_title="3D plotter", layout="wide")

sym_x=smp.symbols("x")
sym_y=smp.symbols("y")

sidebar = st.sidebar
col1, col2, col3 = st.columns([2, 1, 3])

with col1:
    st.header("3D grapher")
    st.divider()
    st.subheader("Function:")
    with st.container(border=True):
            input_function = st.text_input("", placeholder="Write a function f(x,y)")
            c1, c2 = st.columns([1,1])
            with c1:
                 col = st.color_picker("", "#0091f9")

with sidebar:
    st.header("Settings")
    c1, c2, c3= st.columns([1,1,1])
    with c1:
        x_lower= st.number_input("x min", value=-5)
        x_upper = st.number_input("x max", value=5)
    with c2:
        y_lower = st.number_input("y min", value=-5)
        y_upper = st.number_input("y max", value=5)
    with c3:
        z_lower = st.number_input("z min", value=-5)
        z_upper = st.number_input("z max", value=5)   
    st.divider()
    partial = st.checkbox("Compute partial derivatives", value = True)
    try:
        if partial:
            st.latex(r"\frac{\partial f}{\partial x} = " + smp.latex(smp.diff(input_function, sym_x)))
            st.latex(r"\frac{\partial f}{\partial y} = " + smp.latex(smp.diff(input_function, sym_y)))
    except: st.warning(f"Could not differentiate '{input_function}'")
    critical_points= st.checkbox("Find the critical points", value=True)
    try:
        if critical_points:
            expr = smp.parse_expr(input_function)
            critical = smp.solve([smp.diff(expr, sym_x), smp.diff(expr, sym_y)], [sym_x, sym_y])
            critical = [p for p in critical if all(c.is_real for c in p)]
            for point in critical:
                H=smp.hessian(expr, [sym_x, sym_y])
                det = H.det().subs([(sym_x, point[0]), (sym_y, point[1])])
                fxx = smp.diff(expr, sym_x, 2).subs([(sym_x, point[0]), (sym_y, point[1])])
                if det > 0:
                    if fxx > 0:
                        st.write(f"Local minimum at {point}")
                    else:
                        st.write(f"Local maximum at {point}")
                elif det < 0:
                    st.write(f"Saddle point at {point}")
                else:
                    st.write(f"Inconclusive at {point}")
    except Exception as e:
        st.warning(f"Could not compute: {e}")

x=np.linspace(x_lower, x_upper, 100)
y=np.linspace(y_lower, y_upper, 100)
X, Y = np.meshgrid(x, y)
fig=go.Figure()

with col3:
    try:
        f=smp.lambdify([sym_x, sym_y], input_function, modules="numpy")
        Z=f(X,Y)
        fig.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale=[[0, col], [1, col]], name=input_function))
    except:
         with col1:
            st.warning(f"Could not plot '{input_function}'")
fig.update_layout(
            scene=dict(
            xaxis=dict(
                range=[x_lower, x_upper],
                showgrid=True,
                gridwidth=1,
                gridcolor="rgba(200,200,200,0.7)",
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor="black"
            ),
            
            yaxis=dict(
                range=[y_lower, y_upper],
                showgrid=True,
                gridwidth=1,
                gridcolor="rgba(200,200,200,0.7)",
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor="black",
             ),

            zaxis=dict(
                range=[z_lower, z_upper],
                showgrid=True,
                gridwidth=1,
                gridcolor="rgba(200,200,200,0.7)",
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor="black"      
            ),
            ),
            height=700
)

with col3:
    st.plotly_chart(fig, use_container_width=True)
