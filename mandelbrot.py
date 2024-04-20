from lazer import LazerDesign
from math  import e, pi, sqrt

def mandelbrot(c, iterations=400):
    i = 0
    z = 0
    while abs(z) < 2 and i < iterations:
        i += 1
        z = z * z + c

    return abs(z) < 2

def find_start(direction, iterations=100, min=0, max=1, n=0):
    # binary search for the starting position
    length = (min + max)/2
    width  = max - min
    if n >= iterations: return length * direction 

    in_set = mandelbrot(length * direction)
    if not in_set:
        return find_start(direction, iterations, min, min + width/2, n+1)
    else:
        return find_start(direction, iterations, min + width/2, max, n+1)

def find_tangent_angle(pos, direction, iterations=100, min=-pi/2, max=pi/2, n=0):
    # binary search for the tangent angle (given a facing 
    # direction to avoid going backwards)
    angle = (min + max) / 2
    width = max - min 
    if n > iterations: return angle

    new_dir = direction * e**(1j * angle) # rotate by that angle 

    # assume the inside of the set is on the left
    in_set = mandelbrot(pos + new_dir)
    if not in_set:
        return find_tangent_angle(pos, direction, iterations, min, min + width/2, n+1)
    else:
        return find_tangent_angle(pos, direction, iterations, min + width/2, max, n+1)

def fractal_trace(start, direction, dt, nsamples, end_threshold=.4, scale=100):
    # follows an approximation of the tangent to find the border of
    # the fractal set
    path = []
    pos  = start
    direction *= dt
    start_pos = start * scale + 2 * scale * (1+1j)

    for i in range(nsamples):
        angle = find_tangent_angle(pos, direction)
        direction *= e ** (1j * angle)
        pos += direction

        sx = 2 * scale + pos.real * scale
        sy = 2 * scale + pos.imag * scale
        path.append((sx, sy))

        # stop when projected location is within threshold of start position
        dx = sx - start_pos.real 
        dy = sy - start_pos.imag

        min_dist = end_threshold
        if i > nsamples/2 and (dx*dx + dy*dy <= min_dist * min_dist):
            error = sqrt(dx*dx + dy*dy)
            print(f"Endpoint error: {error:.2f}mm")
            break

    path.append((start_pos.real, start_pos.imag)) # close the path so it cuts out properly
    return path

design = LazerDesign()
path = fractal_trace(find_start(1), 1, .003, 5_000, scale=50)
design.polyline(path)
design.save("designs/mandelbrot.svg")
