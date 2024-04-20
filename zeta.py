from lazer import LazerDesign
from math import sqrt

def zeta(s, nterms=40_000):
    # equation (20) from https://mathworld.wolfram.com/RiemannZetaFunction.html
    sum = 0
    for n in range(1, nterms):
        sum += (-1)**(n-1) / (n**s)

    return sum *  1 / (1 - 2**(1-s))

design = LazerDesign()

# measurements (mm)
diameter    = 70
margin      = 3
zeta_scale  = 11
zeta_center = 0.6914518030494091 # averaged the minimum and maximum values of Re(zeta(x)) over the interval
radius      = diameter/2
center      = radius + 5

# draw axes
design.line(
    center - radius + margin, 
    center, 
    center + radius - margin, 
    center, 
    action="engrave"
)

# calculate axis height to preserve circular margin
axis_height = radius - margin
cos_theta   = (zeta_center * zeta_scale) / axis_height # horizontal shift is cos_theta * (radius - margin)
sin_theta   = sqrt(1 - cos_theta**2) # using sin^2 + cos^2 = 1

design.line(
    center - zeta_center * zeta_scale, 
    center - axis_height * sin_theta, 
    center - zeta_center * zeta_scale, 
    center + axis_height * sin_theta, 
    action="engrave"
)

# draw zeta graph
min_val, max_val = 0, 0
start, end  = 0, 34
nsamples    = 1500

points = []
for i in range(nsamples):
    imag = start + (end - start) * i/nsamples
    point = zeta(complex(1/2, imag))

    # scale the graph to look nice
    point -= zeta_center
    point *= zeta_scale
    point += (1-1j) * center

    point = (point.real, -point.imag)
    points.append(point)

design.polyline(points, action="engrave")

# cut out the graph
design.circle(center, center, radius)
design.save("designs/zeta.svg")
