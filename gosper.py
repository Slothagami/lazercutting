from lazer import LazerDesign
from math import pi, e

def trace_path(design, symbols, x, y, step, direction=1):
    path = []
    pos  = complex(x, y)
    turn_angle = pi / 3
    
    for symbol in symbols:
        if symbol == "A" or symbol == "B":
            pos += step * direction
            path.append((pos.real, pos.imag))

        if symbol == "+":
            direction *= e ** (1j * turn_angle)

        if symbol == "-":
            direction *= e ** (-1j * turn_angle)

    design.polyline(path)

def iterate_system(rules, start, iterations):
    pattern = rules[start]

    # needs to replace one for one both types, so it needs its 
    # own loop instead of just replace function
    for _ in range(iterations-1):
        new_pattern = ""
        for symbol in pattern:
            if symbol in rules:
                new_pattern += rules[symbol]
            else: 
                new_pattern += symbol

        pattern = new_pattern

    return pattern


design = LazerDesign()
design.cut_width = 1

n = 4
rules = {"A": "A-B--B+A++AA+B-", "B": "+A-BB--B-A++A+B"}
pattern = iterate_system(rules, "A", n)
trace_path(design, pattern, 500, 500, 1500 * (1/4) ** n)

design.save("designs/gosper.svg")
