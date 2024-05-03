from lazer import LazerDesign
from math import log

def make_carpet(design, size, x, y, n):
    if size <= 2 * lazer_width: return
    if n == 0: return

    # draw center square
    third = size / 3
    design.rect(
        x + third + lazer_width, 
        y + third + lazer_width,
        third - 2 * lazer_width, third - 2 * lazer_width,
        action="cut"
    )

    # recurse all edge tiles
    cords = (0,1,2)
    for xn in cords:
        for yn in cords:
            if xn == yn == 1: continue
            make_carpet(design, size/3, x + third * xn, y + third * yn, n-1)

size = 100 # mm
n    = 5

# calculate depth where is detail can't be printed by the lazer
lazer_width  = 0.12 # mm
max_depth = int(log(lazer_width * 2 / size, 1/3)) # calculates depth where square is twice lazer width. size * (1/3)^n = width

design = LazerDesign()
design.cut_width = .2
make_carpet(design, size, 0, 0, n)
design.rect(-lazer_width, -lazer_width, size + lazer_width, size + lazer_width)
design.save("designs/serpinski-carpet.svg")

print(f"""
    depth: {n}
    max depth: {max_depth}
    n squares: {len(design.elements) + 1}
    Smallest square: {(1/3)**n * size}mm edge
""")
