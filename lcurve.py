from lazer import LazerDesign, LSystem
from math import pi
import json 

# load curve rules
with open("lcurves.json", "r") as file:
    data = json.loads(file.read())

# set parameters
n     = 8
x, y  = 100, 100
width = 5
curve_name = "serpinski-triangle"
curve = data[curve_name]

# generate curve
system = LSystem(
    curve.get("rules"), 
    curve.get("axiom"), 
    curve.get("forward")
)
path = system.trace_path(
    n, x, y, 
    width * float(curve.get("growth_factor")) ** n, 
    pi * float(curve.get("angle_frac"))
)

design = LazerDesign(1)
design.polyline(path)
design.save(f"designs/{curve_name}.svg")
