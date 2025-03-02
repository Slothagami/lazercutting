from math import e
import numpy as np

class LazerDesign:
    def __init__(self, cut_width = .4, width=200, height=200):
        self.elements  = []
        self.cut_width = cut_width

        self.width  = width
        self.height = height

        self.colors = {
            "cut":     "red",
            "engrave": "black",
            "none":    "none"
        }

    def get_color(self, action):
        return self.colors.get(action, "cut")
    
    def element_style(self, action, fill):
        return f'style="stroke: {self.get_color(action)}; fill: {self.get_color(fill)}; stroke-width: {self.cut_width}"'

    def add_element(self, element):
        self.elements.append(element)

    def polyline(self, points, action="cut", fill="none", trim_outside=False, trim_margin=3):
        points_arg = ""
        for point in points:
            x, y = point

            # skip points outside bounding box
            if trim_outside:
                outside_x = not (-trim_margin < x < self.width + trim_margin)
                outside_y = not (-trim_margin < y < self.height + trim_margin)

                if outside_x or outside_y:
                    continue

            points_arg += f" {x},{y}"

        self.add_element(f'<polyline points="{points_arg}" {self.element_style(action, fill)} />')

    def circle(self, cx, cy, radius, action="cut", fill="none"):
        self.add_element(f'<circle cx="{cx}" cy="{cy}" r="{radius}" {self.element_style(action, fill)}  />')

    def line(self, x1, y1, x2, y2, action="cut", fill="none"):
        self.add_element(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" {self.element_style(action, fill)}  />')

    def rect(self, x, y, width, height, border_radius=0, action="cut", fill="none"):
        args = f'x="{x}" y="{y}" width="{width}" height="{height}"'

        if border_radius > 0:
            args += f' rx="{border_radius}" ry="{border_radius}"'
            
        self.add_element(f'<rect {args} {self.element_style(action, fill)}  />')

    def arc(self, x, y, r, start_angle, stop_angle, action, trim_outside=False, precision=100):
        t = np.linspace(start_angle, stop_angle, precision)

        def to_circle_point(t):
            return [x + r * np.cos(t), y + r * np.sin(t)]

        self.polyline(map(to_circle_point, t), action, trim_outside=trim_outside)

    def save(self, filen):
        with open(filen, "w+") as file:
            content = "".join(self.elements)

            # viewBox ensures all units are automatically in mm
            wrapper = f'<svg width="{self.width}mm" height="{self.height}mm" viewBox="0 0 {self.width} {self.height}" xmlns="http://www.w3.org/2000/svg">{content}</svg>'
            file.write(wrapper)


class LSystem:
    def __init__(self, rules, start_state, forward_symbols):
        """
            rules: a dictionary with symbol names linking to their definitions
            start_state: starting symbol

            for tracing fractals defined by iterative rules (usually space filling curve type ones)
        """
        self.rules = rules 
        self.start_state = start_state
        self.forward_symbols = forward_symbols
        self.path = []

    def iterate(self, depth):
        pattern = self.rules[self.start_state]

        # needs to replace one symbol for one both types, so it needs its 
        # own loop instead of just replace function
        for _ in range(depth - 1):
            new_pattern = ""
            for symbol in pattern:
                if symbol in self.rules:
                    new_pattern += self.rules[symbol]
                else: 
                    new_pattern += symbol

            pattern = new_pattern

        return pattern
    
    def trace_path(self, n, x, y, step, turn_angle, direction = 1):
        symbols = self.iterate(n)
        pos  = complex(x, y)
        path = [(x, y)]
        
        for symbol in symbols:
            if symbol in self.forward_symbols:
                pos += step * direction
                path.append((pos.real, pos.imag))

            if symbol == "+":
                direction *= e ** (1j * turn_angle)

            if symbol == "-":
                direction *= e ** (-1j * turn_angle)

        return path

if __name__ == "__main__":
    design = LazerDesign()
    design.polyline([[0,10],[10,20],[20,10]])
    design.polyline([[0,10],[10, 0],[20,10]])
    design.circle(10, 10, 2, "none", "engrave")
    design.rect(22,5,10,10, action="cut", border_radius=2, fill="engrave")
    design.line(17,18, 33, 18)

    # draw engraved zigzag test
    points = []
    for i in range(5):
        points.append([36 + i * 3, 2])
        points.append([36 + i * 3, 18])

    design.polyline(points, "engrave")
    design.save("designs/test.svg")
