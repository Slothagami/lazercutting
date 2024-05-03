from math import e

class LazerDesign:
    def __init__(self, cut_width = .4):
        self.elements = []
        self.cut_width = cut_width
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

    def polyline(self, points, action="cut", fill="none"):
        points_arg = ""
        for point in points:
            points_arg += f" {point[0]},{point[1]}"

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

    def save(self, filen):
        with open(filen, "w+") as file:
            content = "".join(self.elements)
            wrapper = f'<svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">{content}</svg>'
            file.write(wrapper)


class LSystem:
    def __init__(self, rules, start_state):
        """
            rules: a dictionary with symbol names linking to their definitions
            start_state: starting symbol
        """
        self.rules = rules 
        self.start_state = start_state
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
    
    def trace_path(self, symbols, x, y, step, turn_angle, direction = 1):
        path = []
        pos  = complex(x, y)
        
        for symbol in symbols:
            if symbol == "A" or symbol == "B":
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
