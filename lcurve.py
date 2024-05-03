from lazer import LazerDesign, LSystem
from math import pi
import json 

# load curve rules
with open("lcurves.json", "r") as file:
    data = json.loads(file.read())

# set parameters
n     = 4
x, y  = 500, 700
width = 1000
curve_name = "gosper"
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
    pi / int(curve.get("angle_denom"))
)

design = LazerDesign(1)
design.polyline(path)
design.save(f"designs/{curve_name}.svg")
