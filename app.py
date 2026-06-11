import numpy as np
import chart_studio.plotly as py
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import sympy as smp

st.set_page_config(page_title="Graphing Calculator", layout="wide")

sym_x=smp.symbols("x")

sidebar = st.sidebar
col1, col2 = st.columns([1, 3])

if "blocks" not in st.session_state:
        st.session_state.blocks=[{"text": "", "color": "#0091f9"}]

def add_block(index, current_text, current_color):
    st.session_state.blocks[index]["text"] = current_text
    st.session_state.blocks[index]["color"] = current_color
    st.session_state.blocks.insert(index + 1, {"text": current_text, "color": current_color})

def mikami(index):
    st.session_state.blocks.pop(index)

with col1:
    st.header("Graphing Calculator")
    st.divider()
    st.subheader("Functions:")
    for i, block in enumerate(st.session_state.blocks):
        with st.container(border=True):
            input_function = st.text_input("", value=block["text"], key=f"text_{i}")
            st.session_state.blocks[i]["text"] = input_function
            c1, c2 = st.columns([1, 1])
            with c1:
                col = st.color_picker("Pick a color", block["color"], key=f"color_{i}")
                st.session_state.blocks[i]["color"] = col
            with c2:
                st.write("")
                st.write("")
                st.button(
                    "Insert new function",
                    key=f"btn_{i}",
                    on_click=add_block,
                    args=(i, input_function, col)
                )
                if len(st.session_state.blocks) > 1:
                    st.button(
                        "DELETE",
                        key=f"del_{i}",
                        on_click=mikami,
                        args=(i,),
                    )
with sidebar:
    st.header("Settings")
    c1, c2= st.columns([1,1])
    with c1:
        x_lower= st.number_input("x min", value=-5)
        x_upper = st.number_input("x max", value=5)
    with c2:
        y_lower = st.number_input("y min", value=-5)
        y_upper = st.number_input("y max", value=5)
    st.subheader("Display")
    showgrid=st.checkbox("Show grid", value=True)
    showzero=st.checkbox("Show axis lines", value=True)
    st.divider()
    st.subheader("Analysis tools")
    derivative=st.checkbox("Show derivative", value=False)
    if derivative:
        for block in st.session_state.blocks:
            expr_str=block["text"]
            color=block["color"]
            st.write("f'(",expr_str,")=",smp.diff(expr_str))
    zeros=st.checkbox("Show zeros", value=False)
    if zeros:
        for block in st.session_state.blocks:
            expr_str=block["text"]
            color=block["color"]
            st.write("Zeros of the function ", expr_str, ":")
            sols = smp.solve(expr_str,sym_x)
            realsols = [sol for sol in sols if sol.is_real]
            a= ""
            for zero in realsols:
                a += str(zero) + ", "
            st.write(a)
            if len(realsols) == 0:
                st.write("∅")

x=np.linspace(-1000, 1000, 100000)
fig=go.Figure()

for block in st.session_state.blocks:
    expr_str=block["text"]
    color=block["color"]
    if not expr_str.strip():
        continue
    try: 
        sympy_expression = smp.parse_expr(expr_str)
        f=smp.lambdify(sym_x, sympy_expression, modules="numpy")
        y = np.array([float(f(val)) for val in x])
        dy=np.abs(np.diff(y))
        y[:-1][dy > 100] = np.nan
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name=expr_str,
                                line=dict(color=color, width=4)))
        
        if derivative:
            diff = smp.lambdify(sym_x, smp.diff(sympy_expression),  modules="numpy")
            d = np.array([float(diff(val)) for val in x])
            dd=np.abs(np.diff(d))
            d[:-1][dd > 100] = np.nan
            fig.add_trace(go.Scatter(x=x, y=d, mode='lines', name=("d/dx"),
                                    line=dict(color=color, width=4, dash="dash")))

    except Exception as e:
        with col1:
            st.warning(f"Could not plot '{expr_str}'")

fig.update_layout(
    hovermode="x unified",
    template="plotly_white", 
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
        zerolinecolor="black"
    ),
    plot_bgcolor="white",
    height=800
)

if not showzero:
    fig.update_layout(xaxis=dict(zeroline=False), yaxis=dict(zeroline=False))
if not showgrid:
    fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))



with col2:
    st.plotly_chart(fig, use_container_width=True)