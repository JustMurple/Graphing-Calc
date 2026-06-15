import numpy as np
import plotly.graph_objects as go
import streamlit as st
import sympy as smp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

st.set_page_config(page_title="Graphing Calculator", layout="wide")

transformations = (
    standard_transformations +
    (implicit_multiplication_application,) +
    (convert_xor,)
)


sym_x=smp.symbols("x")

sidebar = st.sidebar
col1, col2 = st.columns([1, 3])

if "blocks" not in st.session_state:
        st.session_state.blocks=[{"text": "", "color": "#0091f9", "show": True}]

def add_block(index, current_text, current_color, show_btn):
    st.session_state.blocks[index]["show"] = show_btn
    st.session_state.blocks[index]["text"] = current_text
    st.session_state.blocks[index]["color"] = current_color
    st.session_state.blocks.insert(index + 1, {"text": current_text, "color": current_color, "show": True})

def mikami(index):
    st.session_state.blocks.pop(index)

with col1:
    st.header("Graphing Calculator")
    st.divider()
    st.subheader("Functions:")
    for i, block in enumerate(st.session_state.blocks):
        with st.container(border=True):
            cu1, cu2, cu3 = st.columns([1,3,1])
            with cu1:
                show = st.checkbox("", value=block["show"], key=f"show_{i}", label_visibility="collapsed")
            with cu3:
                if len(st.session_state.blocks) > 1:
                    st.button(
                        "🗑️",
                        key=f"del_{i}",
                        on_click=mikami,
                        args=(i,),
                    )
            st.session_state.blocks[i]["show"] = show
            input_function = st.text_input("", value=block["text"], key=f"text_{i}", label_visibility="collapsed")
            st.session_state.blocks[i]["text"] = input_function
            c1, c2, c3 = st.columns([1, 3, 1])
            with c1:
                col = st.color_picker("", block["color"], key=f"color_{i}", label_visibility="collapsed")
                st.session_state.blocks[i]["color"] = col
            with c3:
                st.button(
                    "➕",
                    key=f"btn_{i}",
                    on_click=add_block,
                    args=(i, input_function, col, show)
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
    avg = st.checkbox("Show average value", value=False)
    if avg:
        try:
            with st.expander("", expanded=True):
                for i, block in enumerate(st.session_state.blocks):
                    expr_str=block["text"]
                    color=block["color"]
                    sympy_expression = smp.parse_expr(expr_str, transformations=transformations, local_dict={"e": smp.E}) 
                    co1, co2 = st.columns([1,1])
                    with co1:
                        a=st.number_input(f"lower bound of {sympy_expression}", value=0, key=f"lower {i}")
                    with co2:
                        b=st.number_input(f"upper bound of {sympy_expression}", value=1, key = f"upper {i}")
                    try:
                        if b-a != 0:
                            average = (1/(b-a))*smp.integrate((sympy_expression), (sym_x, a, b))
                            st.write(f"avg. value of {sympy_expression} between {a} and {b}")
                            st.latex(float(average))
                        else:
                            st.write(f"avg. value of {sympy_expression} between {a} and {b}")
                            f=smp.lambdify(sym_x, sympy_expression, modules="numpy")
                            st.latex(f(a))
                    except:
                        st.warning(f"Couldn't evaluate avg. value between {a} and {b}")
        except:
            st.warning("Please insert a function of x")
    derivative=st.checkbox("Show derivative", value=False)
    if derivative:
        try:
            with st.expander("", expanded=True):
                for block in st.session_state.blocks:
                    expr_str=block["text"]
                    color=block["color"]
                    sympy_expression = smp.parse_expr(expr_str, transformations=transformations, local_dict={"e": smp.E})
                    st.write("f'(",expr_str,")=",smp.diff(sympy_expression))
        except:
            st.warning("Please insert a function of x")
    zeros=st.checkbox("Show zeros", value=False)
    if zeros:
        try:
            with st.expander("", expanded=True):
                for block in st.session_state.blocks:
                    expr_str=block["text"]
                    color=block["color"]
                    sympy_expression = smp.parse_expr(expr_str, transformations=transformations, local_dict={"e": smp.E})
                    st.write("Zeros of the function ", expr_str, ":")
                    sols = smp.solve(sympy_expression,sym_x)
                    realsols = [sol for sol in sols if sol.is_real]
                    a= ""
                    for zero in realsols:
                        a += str(zero) + ", "
                    st.write(a)
                    if len(realsols) == 0:
                        st.write("∅")
        except:
            st.warning("Please insert a function of x")
    arc = st.checkbox("Compute arc length", value=False)
    if arc:
        try:
            with st.expander("", expanded=True):
                for i, block in enumerate(st.session_state.blocks):
                    expr_str=block["text"]
                    color=block["color"]
                    sympy_expression = smp.parse_expr(expr_str, transformations=transformations, local_dict={"e": smp.E})
                    try:
                        c1, c2 = st.columns([1,1])
                        with c1:
                            a=st.number_input("Insert lower bound", value=0, key=f"lowarc{i}")
                        with c2:
                            b=st.number_input("Insert upper bound", value=1, key=f"uparc{i}")
                        inte = smp.integrate((smp.sqrt(1+(smp.diff(sympy_expression, sym_x))**2)), (sym_x, a, b))
                        st.write(f"Arc length of {sympy_expression} between {a} and {b} =")
                        st.latex(inte)
                        st.write("or")
                        try:
                            st.latex(float(inte))
                        except:
                            st.warning("Couldn't convert to decimal")
                    except:
                        st.warning("Couldn't compute")
        except:
            st.warning("Please insert a function of x")

x=np.linspace(-1000, 1000, 100000)
fig=go.Figure()

for block in st.session_state.blocks:
    expr_str=block["text"]
    color=block["color"]
    shown=block["show"]
    if not expr_str.strip():
        continue
    try:
        if shown:
            sympy_expression = smp.parse_expr(expr_str, transformations=transformations, local_dict={"e": smp.E})
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
                fig.add_trace(go.Scatter(x=x, y=d, mode='lines', name=(f"d/dx ({expr_str})"),
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