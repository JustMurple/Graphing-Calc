Axis

Four interactive math tools in one place. Plot functions, visualize 3D surfaces, compute calculations symbolically, and view vector fields

Tools:

Graphing Calculator — plot multiple functions at once with a color picker for each one. Toggle on derivatives (plotted as dashed lines), find zeros, compute average values over an interval, and calculate arc lengths. Supports sin, cos, tan, log, e^x, sqrt, and anything else SymPy can parse.

3D Plotter — visualize surfaces f(x, y) as interactive 3D meshes. Finds critical points using the Hessian determinant and classifies them as local minima, maxima, or saddle points. Computes partial derivatives symbolically.

Calculator — symbolic computation for single-variable and multi-variable functions: indefinite and definite integrals, derivatives, limits (including ±∞), double integrals, and triple integrals supporting all six orders of integration.

Vector Fields — plots 2D vector fields F = <U, V> as quiver plots. Computes curl and divergence symbolically, finds the potential function if the field is conservative, and evaluates work and flux integrals along a parametric curve.


Try these

# Graphing calculator
sin(x)/x, 
x^3 - 2*x, 
e^(-x^2)

# 3D plotter
sin(x)*cos(y),
x^2 - y^2,
e^(-(x^2 + y^2))

# Vector fields
U = -y,  V = x       ← rotation field, curl = 2;
U = x,   V = y; 
U = y,   V = x       ← conservative, curl = 0, the potential function is computed automatically when "compute curl" option is selected


How it works

Everything symbolic goes through SymPy. That means results like ∫ sin(x²) dx come back as actual closed-form expressions, not just floating-point approximations 

Input parsing uses SymPy's implicit_multiplication_application and convert_xor transformations, so 2x, x^2, and e all work the way you'd write them on paper.

Plotting is done with Plotly — the 2D tracer handles discontinuities by masking points where |Δy| > 100 between samples, which catches vertical asymptotes cleanly without needing to know where they are analytically. The 3D plotter does the same along both mesh axes.

The vector field visualizer uses plotly.figure_factory.create_quiver. The grid density stays fixed at 20×20 while the domain adjusts, so you don't get 10,000 arrows when you zoom in.


Run locally

bashgit clone https://github.com/yourusername/math-tools
cd math-tools
pip install streamlit sympy numpy plotly
streamlit run Home.py

Requires Python 3.9+.


Streamlit — UI and multi-page routing
SymPy — symbolic math
NumPy — numerical evaluation
Plotly — interactive plots
