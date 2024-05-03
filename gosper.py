from lazer import LazerDesign, LSystem
from math import pi

rules = {
    "A": "A-B--B+A++AA+B-", 
    "B": "+A-BB--B-A++A+B"
}

gosper = LSystem(rules, "A")
n      = 4
path   = gosper.trace_path(n, 500, 500, 1500 * (1/4)**n, pi/3)

design = LazerDesign(1)
design.polyline(path)
design.save("designs/gosper.svg")
