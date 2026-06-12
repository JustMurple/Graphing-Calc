import plotly.figure_factory as ff
import numpy as np
import chart_studio.plotly as py
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import sympy as smp

st.set_page_config(page_title="Vector Fields", layout="wide")

x, y = np.meshgrid(np.linspace(-2, 2, 20), np.linspace(-2, 2, 20))
sym_x, sym_y, t = smp.symbols("x , y, t")


sidebar = st.sidebar
col1, col2, col3 = st.columns([2, 1, 3])

with col1:
    st.header("Vector field visualizer")
    st.divider()
    st.subheader("Enter your vector field")
    with st.container(border=True):
        U=st.text_input("F<U, V>", placeholder="U")
        V=st.text_input("", placeholder="V")

with sidebar:
    curl = st.checkbox("Compute curl")
    if curl:
        try:
            vx = smp.diff(V, sym_x)
            uy = smp.diff(U, sym_y)
            curle = smp.simplify(vx-uy)
            st.latex(rf"\operatorname{{curl}}(\vec{{F}}) = {smp.latex(curle)}")
            if curle == 0:
                gv = smp.parse_expr(V)
                gu = smp.parse_expr(U)
                pot = smp.integrate(gu, sym_x)
                pot += smp.integrate(gv - smp.diff(pot, sym_y), sym_y)
                st.latex(rf"""\begin{{aligned}}
                \nabla f &= \vec{{F}} \\
                \text{{where }} f &= {smp.latex(pot)}
                \end{{aligned}}
                """)
        except Exception as e:
            st.error("Engine failure details:")
            st.exception(e)
    div = st.checkbox("Compute divergence")
    if div:
        try:
            ux = smp.diff(U, sym_x)
            vy = smp.diff(V, sym_y)
            st.latex(rf"\operatorname{{div}}(\vec{{F}}) = {ux+vy}")
        except:
            st.warning("Couldn't compute")
    work = st.checkbox("Compute work integral")
    if work:
        xt_s = st.text_input("Insert t parametrization for x")
        yt_s = st.text_input("Insert t parametrization for y")
        ts_s = st.text_input("Insert starting value of t")
        tf_s = st.text_input("Insert ending value of t")
        if xt_s and yt_s and ts_s and tf_s:
                try:
                    xt = smp.parse_expr(xt_s)
                    yt = smp.parse_expr(yt_s)
                    ts = smp.parse_expr(ts_s)
                    tf = smp.parse_expr(tf_s)
                    usmp=smp.parse_expr(U)
                    vsmp=smp.parse_expr(V)
                    dtx = smp.diff(xt, t)
                    dty = smp.diff(yt, t)
                    ut = usmp.subs({sym_x: xt, sym_y: yt})
                    vt = vsmp.subs({sym_x: xt, sym_y: yt})
                    integrand = ut*dtx + vt*dty
                    integrandl = smp.latex(integrand)
                    res = smp.integrate(integrand, (t, ts, tf))
                    st.latex(rf"\int_{{{smp.latex(ts)}}}^{{{smp.latex(tf)}}} \left( {integrandl} \right) dt =")
                    st.latex(res)
                except:
                    st.warning("Couldn't compute")
    flux = st.checkbox("Compute flux integral")
    if flux: 
        xt_s = st.text_input("Insert t parametrization for x ")
        yt_s = st.text_input("Insert t parametrization for y ")
        ts_s = st.text_input("Insert starting value of t ")
        tf_s = st.text_input("Insert ending value of t ")
        if xt_s and yt_s and ts_s and tf_s:
            try:
                xt = smp.parse_expr(xt_s)
                yt = smp.parse_expr(yt_s)
                ts = smp.parse_expr(ts_s)
                tf = smp.parse_expr(tf_s)
                usmp=smp.parse_expr(U)
                vsmp=smp.parse_expr(V)
                dtx = smp.diff(xt, t)
                dty = smp.diff(yt, t)
                ut = usmp.subs({sym_x: xt, sym_y: yt})
                vt = vsmp.subs({sym_x: xt, sym_y: yt})
                integrand = ut*dty - vt*dtx
                integrandl = smp.latex(integrand)
                res = smp.integrate(integrand, (t, ts, tf))
                st.latex(rf"\int_{{{smp.latex(ts)}}}^{{{smp.latex(tf)}}} \left( {integrandl} \right) dt =")
                st.latex(res)
            except:
                st.warning("Couldn't compute")
fig = None
uf=smp.lambdify([sym_x, sym_y], U, modules="numpy")
vf=smp.lambdify([sym_x, sym_y], V, modules="numpy")

try:
    u=uf(x,y)
    v=vf(x,y)
    fig = ff.create_quiver(x, y, u, v, scale=0.1)
except:
    with col1:
        st.warning("Insert functions of x, y in the boxes")  

with col3:
    if fig is not None:
        st.plotly_chart(fig, use_container_width=True)