import plotly.figure_factory as ff
import numpy as np
import streamlit as st
import sympy as smp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor


st.set_page_config(page_title="Vector Fields", layout="wide")

transformations = (
    standard_transformations +
    (implicit_multiplication_application,) +
    (convert_xor,)
)


sym_x, sym_y, t = smp.symbols("x , y, t")


sidebar = st.sidebar
col1, col2, col3 = st.columns([2, 1, 3])

with col1:
    st.header("Vector field visualizer")
    st.divider()
    st.subheader("Enter your vector field")
    with st.container(border=True):
        U_inp=st.text_input("F<U, V>", placeholder="U")
        try:
            U=smp.parse_expr(U_inp, transformations=transformations, local_dict={"e": smp.E})
        except:
            pass
        V_inp=st.text_input("", placeholder="V")
        try:
            V=smp.parse_expr(V_inp, transformations=transformations, local_dict={"e": smp.E})
        except:
            pass

with sidebar:
    st.header("Settings")
    c1, c2= st.columns([1,1])
    with c1:
        xlow= st.number_input("x min", value=-2)
        xup = st.number_input("x max", value=2)
    with c2:
        ylow = st.number_input("y min", value=-2)
        yup = st.number_input("y max", value=2)
    st.divider()
    st.header("Analysis tools")
    curl = st.checkbox("Compute curl")
    if curl:
        try:
            with st.expander("", expanded=True):
                try:
                    vx = smp.diff(V, sym_x)
                    uy = smp.diff(U, sym_y)
                    curle = smp.simplify(vx-uy)
                    st.latex(rf"\operatorname{{curl}}(\vec{{F}}) = {smp.latex(curle)}")
                    if curle == 0:
                        pot = smp.integrate(U, sym_x)
                        pot += smp.integrate(V - smp.diff(pot, sym_y), sym_y)
                        st.latex(rf"""\begin{{aligned}}
                        \nabla f &= \vec{{F}} \\
                        \text{{where }} f &= {smp.latex(pot)}
                        \end{{aligned}}
                        """)
                except Exception as e:
                    st.warning("Couldn't compute")
        except:
            st.warning("Please insert functions of x,y")
    div = st.checkbox("Compute divergence")
    if div:
        try:
            with st.expander("", expanded=True):
                try:
                    ux = smp.diff(U, sym_x)
                    vy = smp.diff(V, sym_y)
                    latexdiv = smp.latex(ux+vy)
                    st.latex(rf"\operatorname{{div}}(\vec{{F}}) = {latexdiv}")
                except:
                    st.warning("Couldn't compute")
        except:
            st.warning("Please insert functions of x,y")
    work = st.checkbox("Compute work integral")
    if work:
        with st.expander("", expanded=True):
            xt_s = st.text_input("Insert t parametrization for x")
            yt_s = st.text_input("Insert t parametrization for y")
            ts_s = st.text_input("Insert starting value of t")
            tf_s = st.text_input("Insert ending value of t")
            if xt_s and yt_s and ts_s and tf_s:
                    try:
                        xt = smp.parse_expr(xt_s, transformations=transformations, local_dict={"e": smp.E})
                        yt = smp.parse_expr(yt_s, transformations=transformations, local_dict={"e": smp.E})
                        ts = smp.parse_expr(ts_s, transformations=transformations, local_dict={"e": smp.E})
                        tf = smp.parse_expr(tf_s, transformations=transformations, local_dict={"e": smp.E})
                        dtx = smp.diff(xt, t)
                        dty = smp.diff(yt, t)
                        ut = U.subs({sym_x: xt, sym_y: yt})
                        vt = V.subs({sym_x: xt, sym_y: yt})
                        integrand = ut*dtx + vt*dty
                        integrandl = smp.latex(integrand)
                        res = smp.integrate(integrand, (t, ts, tf))
                        st.latex(rf"\int_{{{smp.latex(ts)}}}^{{{smp.latex(tf)}}} \left( {integrandl} \right) dt =")
                        st.latex(res)
                    except:
                        st.warning("Couldn't compute")
    flux = st.checkbox("Compute flux integral")
    if flux:
        with st.expander("", expanded=True):
            xt_s = st.text_input("Insert t parametrization for x ")
            yt_s = st.text_input("Insert t parametrization for y ")
            ts_s = st.text_input("Insert starting value of t ")
            tf_s = st.text_input("Insert ending value of t ")
            if xt_s and yt_s and ts_s and tf_s:
                try:
                    xt = smp.parse_expr(xt_s, transformations=transformations, local_dict={"e": smp.E})
                    yt = smp.parse_expr(yt_s, transformations=transformations, local_dict={"e": smp.E})
                    ts = smp.parse_expr(ts_s, transformations=transformations, local_dict={"e": smp.E})
                    tf = smp.parse_expr(tf_s, transformations=transformations, local_dict={"e": smp.E})
                    dtx = smp.diff(xt, t)
                    dty = smp.diff(yt, t)
                    ut = U.subs({sym_x: xt, sym_y: yt})
                    vt = V.subs({sym_x: xt, sym_y: yt})
                    integrand = ut*dty - vt*dtx
                    integrandl = smp.latex(integrand)
                    res = smp.integrate(integrand, (t, ts, tf))
                    st.latex(rf"\int_{{{smp.latex(ts)}}}^{{{smp.latex(tf)}}} \left( {integrandl} \right) dt =")
                    st.latex(res)
                except:
                    st.warning("Couldn't compute")
fig = None
x, y = np.meshgrid(np.linspace(xlow, xup, 20), np.linspace(ylow, yup, 20))

try:
    uf=smp.lambdify([sym_x, sym_y], U, modules="numpy")
    vf=smp.lambdify([sym_x, sym_y], V, modules="numpy")
except:
    pass
if U_inp and V_inp:
    try:
        u=uf(x,y)
        v=vf(x,y)
        fig = ff.create_quiver(x, y, u, v, scale=0.1)
        fig.update_xaxes(range=[xlow, xup])
        fig.update_yaxes(range=[ylow, yup])
    except:
        with col1:
            st.warning("Insert functions of x, y in the boxes")  

with col3:
    if fig is not None:
        st.plotly_chart(fig, use_container_width=True)