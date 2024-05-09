from lazer import LazerDesign
from math import log

def make_carpet(design, size, x, y, n):
    if size <= lazer_width: return
    if n == 0: return

    # draw center square
    third = size / 3
    if third - 2 * lazer_width <= 0: 
        # end here and draw dot
        x += size/2
        y += size/2
        design.rect(
            x - min_size/2, # adding lazer width to account for the kerf
            y - min_size/2,
            min_size, min_size,
            action="cut"
        )
        return

    design.rect(
        x + third + lazer_width, # adding lazer width to account for the kerf
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
n    = 6
# size = 100/(3**2) # mm
# n    = 4

# calculate depth where is detail can't be printed by the lazer
lazer_width = 0.13 # mm (half the width of the lazer)
min_size    = 0.04
max_depth   = int(log(lazer_width * 2 / size, 1/3)) # calculates depth where square is twice lazer width. size * (1/3)^n = width

design = LazerDesign(.05)
make_carpet(design, size, 0, 0, n)

design.rect(-lazer_width, -lazer_width, size + lazer_width * 2, size + lazer_width * 2)
design.save("designs/serpinski-carpet.svg")

print(f"""
    depth: {n}
    max depth: {max_depth}
    n squares: {len(design.elements) + 1}
    Smallest square: {(1/3)**n * size}mm edge
""")
