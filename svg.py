import lxml.html
import turtle

def open_svg(file_name):
    with open(file_name, "r") as input_fp:
        svg_xml = input_fp.read()
    return svg_xml


def rect_or_square(width, height):
    t = turtle.Turtle()
    for i in range(2):
        t.forward(width)
        t.left(90)
        t.forward(height)
        t.left(90)
    input("Hit enter to close turtle window")
    t.screen.bye()
    return None

svg_xml = open_svg("rect.svg")
svg_root = lxml.html.fromstring(svg_xml)

# Parsing Rectangle - https://www.w3schools.com/graphics/svg_rect.asp
# Rectangle xpath selector = "//rect"
# Attributes to check:
#   width, height
#   x, y position
#   rx, ry

rect_element = svg_root.xpath("//rect")
rect_element = rect_element[0]
rect_x = rect_element.attrib.get("x")
rect_rx = rect_element.attrib.get("rx")
rect_y = rect_element.attrib.get("y")
rect_ry = rect_element.attrib.get("ry")
rect_width = int(rect_element.attrib.get("width"))
rect_height = int(rect_element.attrib.get("height"))

print(f"X: {rect_x}, Y: {rect_y}")
print(f"RX: {rect_rx}, RY: {rect_ry}")
print(f"Width: {rect_width}, Height: {rect_height}")

rect_or_square(width=rect_width, height=rect_height)



# class Draw(object):
#     def __init__(self):
#         return NOne
