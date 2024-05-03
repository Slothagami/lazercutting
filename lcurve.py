from lazer import LazerDesign, LSystem
from math import pi
import json 

# load curve rules
with open("lcurves.json", "r") as file:
    data = json.loads(file.read())

# set parameters
n      = 4
x, y = 500, 500
curve_name = "hilbert"
curve = data[curve_name]

# generate curve
gosper = LSystem(
    curve.get("rules"), 
    curve.get("axiom"), 
    curve.get("forward")
)
path = gosper.trace_path(
    n, x, y, 1500 * (1/4)**n, 
    pi / int(curve.get("angle_denom"))
)

design = LazerDesign(1)
design.polyline(path)
design.save(f"designs/{curve_name}.svg")
