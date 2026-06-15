import numpy as np
import plotly.graph_objects as go
import streamlit as st
import sympy as smp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

st.set_page_config(page_title="3D plotter", layout="wide")

transformations = (
    standard_transformations +
    (implicit_multiplication_application,) +
    (convert_xor,)
)

sym_x=smp.symbols("x")
sym_y=smp.symbols("y")

sidebar = st.sidebar
col1, col2, col3 = st.columns([2, 1, 4])

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
    st.header("3D grapher")
    st.divider()
    st.subheader("Function:")
    for i, block in enumerate(st.session_state.blocks):
        with st.container(border=True):
            cu1, cu2, cu3 = st.columns([1,3,1])
            with cu1:
                show = st.checkbox("", value=block["show"], key=f"show_{i}", label_visibility="collapsed")
                st.session_state.blocks[i]["show"] = show
            with cu3:
                if len(st.session_state.blocks) > 1:
                    st.button(
                        "🗑️",
                        key=f"del_{i}",
                        on_click=mikami,
                        args=(i,),
                    )
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
    st.header("Analysis tools")
    partial = st.checkbox("Compute partial derivatives", value = False)
    
    if partial:
            try:
                with st.expander("", expanded=True):
                    for block in st.session_state.blocks:
                        expr_str=block["text"]
                        color=block["color"]
                        try:
                            symp = smp.parse_expr(expr_str, transformations=transformations, local_dict={"e": smp.E})
                            st.latex(r"\frac{\partial}{\partial x}" + r"\left(" + smp.latex(symp) + r"\right)" + "=" + smp.latex(smp.diff(symp, sym_x)))
                            st.latex(r"\frac{\partial}{\partial y}" + r"\left(" + smp.latex(symp) + r"\right)" + "=" + smp.latex(smp.diff(symp, sym_y)))
                        except: 
                            st.warning(f"Could not differentiate '{smp.latex(symp)}'")
            except:
                st.warning("Please insert a function of x,y")
    critical_points= st.checkbox("Find the critical points", value = False)
    try:
        if critical_points:
            try:
                with st.expander("", expanded=True):
                    for block in st.session_state.blocks:
                        expr_str=block["text"]
                        color=block["color"]
                        expr = smp.parse_expr(expr_str, transformations=transformations, local_dict={"e": smp.E})
                        critical = smp.solve(
                        [smp.diff(expr, sym_x), smp.diff(expr, sym_y)],
                        [sym_x, sym_y],
                        dict=True
                        )
                        critical = [
                        (sol[sym_x], sol[sym_y])
                        for sol in critical
                        if sol[sym_x].is_real is not False
                        and sol[sym_y].is_real is not False
                        ]
                        for point in critical:
                            H=smp.hessian(expr, [sym_x, sym_y])
                            det = float(H.det().subs([(sym_x, point[0]), (sym_y, point[1])]))
                            fxx = float(smp.diff(expr, sym_x, 2).subs([(sym_x, point[0]), (sym_y, point[1])]))
                            if det > 0:
                                if fxx > 0:
                                    st.write(expr, f"Local minimum at {point}")
                                else:
                                    st.write(expr, f"Local maximum at {point}")
                            elif det < 0:
                                st.write(expr, f"Saddle point at {point}")
                            else:
                                st.write(expr, f" Inconclusive at {point}")
            except Exception as e:
                st.warning(f"Could not compute")
    except: 
        st.warning("Please insert a function of x,y")

x=np.linspace(x_lower, x_upper, 100)
y=np.linspace(y_lower, y_upper, 100)
X, Y = np.meshgrid(x, y)
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
            f=smp.lambdify([sym_x, sym_y], sympy_expression, modules="numpy")
            Z = np.array([[float(f(x_val, y_val)) for x_val in x] for y_val in y])
            dz_x = np.abs(np.diff(Z, axis=1))
            dz_y = np.abs(np.diff(Z, axis=0))
            threshold = 100
            Z[:, :-1][dz_x > threshold] = np.nan 
            Z[:, 1:][dz_x > threshold] = np.nan
            Z[:-1, :][dz_y > threshold] = np.nan 
            Z[1:, :][dz_y > threshold] = np.nan
            fig.add_trace(go.Surface(
                x=X, y=Y, z=Z,
                colorscale=[[0, color], [1, color]], 
                showscale=False, 
                name=expr_str
))
    except:
        with col1:
            st.warning(f"Could not plot '{expr_str}'")
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
