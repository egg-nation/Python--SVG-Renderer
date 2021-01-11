import lxml.html
# import turtle
from PIL import Image, ImageDraw

IMAGE_WIDTH = 1000
IMAGE_HEIGHT = 500
FILE_NAME = "rect.svg"


def draw_rect_square(pos_x, pos_y, width, height):
    img = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))
    draw = ImageDraw.Draw(img)
    # https://note.nkmk.me/en/python-pillow-imagedraw/
    rect_top_left_coords = (pos_x, pos_y)
    rect_bottom_right_coords = (pos_x + width, pos_y + height)
    draw.rectangle((rect_top_left_coords, rect_bottom_right_coords), outline="green")
    img.show()
    return img

def open_svg(FILE_NAME):
    with open(FILE_NAME, "r") as input_fp:
        svg_xml = input_fp.read()
    return svg_xml


# def rect_or_square(width, height, ttle):
#     t = ttle
#     for i in range(2):
#         t.forward(width)
#         t.right(90)
#         t.forward(height)
#         t.right(90)
#     input("Hit enter to close turtle window")
#     t.screen.bye()
#     return None

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
rect_x = int(rect_element.attrib.get("x"))
rect_rx = rect_element.attrib.get("rx")
rect_y = int(rect_element.attrib.get("y"))
rect_ry = rect_element.attrib.get("ry")
rect_width = int(rect_element.attrib.get("width"))
rect_height = int(rect_element.attrib.get("height"))

print(f"X: {rect_x}, Y: {rect_y}") 
print(f"RX: {rect_rx}, RY: {rect_ry}")
print(f"Width: {rect_width}, Height: {rect_height}")

img = draw_rect_square(rect_x, rect_y, rect_width, rect_height)
img.save(FILE_NAME.replace(".svg", ".png"))


# Move turtle to specific coordinates (x,y)
# Assuming top left as (0,0)
# def goto_coord(x, y, ttle):
#     ttle.penup()
#     ttle.goto(x - ttle.screen.window_width()/2, ttle.screen.window_height()/2 - y)
#     ttle.pendown()
#     return None

# ttle = turtle.Turtle()
# goto_coord(rect_x, rect_y, ttle)
# rect_or_square(width=rect_width, height=rect_height, ttle=ttle)

# class Draw(object):
#     def __init__(self):
#         return NOne
