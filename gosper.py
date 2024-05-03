from lazer import LazerDesign, LSystem
from math import pi

design = LazerDesign(1)

rules = {
    "A": "A-B--B+A++AA+B-", 
    "B": "+A-BB--B-A++A+B"
}
gosper = LSystem(rules, "A")

n = 4
pattern = gosper.iterate(n)
path    = gosper.trace_path(pattern, 500, 500, 1500 * (1/4) ** n, pi/3)

design.polyline(path)
design.save("designs/gosper.svg")
