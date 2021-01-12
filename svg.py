import lxml.html
# import turtle
from PIL import Image, ImageDraw

IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1080
FILE_NAME = "rect.svg"
# FILE_NAME = "cir.svg"
# FILE_NAME = "el.svg"
# FILE_NAME = "ln.svg"
# FILE_NAME = "combined.svg"
# FILE_NAME = "poly_ln.svg"

def open_svg(file):
    with open(file, "r") as input_fp:
        svg_xml = input_fp.read()
    return svg_xml

def get_fill_outline(element):
    print(f"Analysing style attributes")
    style = str(element.attrib.get("style"))
    print(f"Got style: {style}")
    if style == "None":
        fill = str(element.attrib.get("fill"))
        if fill == "none":
           fill = (255, 255, 255, 0)
        stroke = str(element.attrib.get("stroke"))
        if stroke == "none":
           stroke = (255, 255, 255, 0)
        stroke_width = int(element.attrib.get("stroke-width"))
        print(f"Fill and stroke in style: {fill}, {stroke}, {stroke_width}")
        return fill, stroke, stroke_width
    else:
        attr_dict = {pair.split(":")[0]: pair.split(":")[1] for pair in style.split(";")}
        print(f"Style dictionary: {attr_dict}")
        fill = attr_dict['fill']
        if fill == "none":
           fill = (255, 255, 255, 0)
        stroke = attr_dict['stroke']
        if stroke == "none":
           stroke = (255, 255, 255, 0)
        stroke_width = int(attr_dict['stroke-width'])
        print(f"Fill and stroke in style: {fill}, {stroke}, {stroke_width}")
        return fill, stroke, stroke_width

def get_fill_lines(element):
    print(f"Analysing style attributes")
    style = str(element.attrib.get("style"))
    print(f"Got style: {style}")
    if style == "None":
        stroke = str(element.attrib.get("stroke"))
        if stroke == "none":
           stroke = (255, 255, 255, 0)
        stroke_width = int(element.attrib.get("stroke-width"))
        print(f"Fill and stroke in style: {stroke}, {stroke_width}")
        return stroke, stroke_width
    else:
        attr_dict = {pair.split(":")[0]: pair.split(":")[1] for pair in style.split(";")}
        print(f"Style dictionary: {attr_dict}")
        stroke = attr_dict['stroke']
        if stroke == "none":
           stroke = (255, 255, 255, 0)
        stroke_width = int(attr_dict['stroke-width'])
        print(f"Fill and stroke in style: {stroke}, {stroke_width}")
        return stroke, stroke_width

def draw_rect_square(img, pos_x, pos_y, width, height, fill, stroke, stroke_width):
    draw = ImageDraw.Draw(img)
    # https://note.nkmk.me/en/python-pillow-imagedraw/
    rect_top_left_coords = (pos_x, pos_y)
    rect_bottom_right_coords = (pos_x + width, pos_y + height)
    draw.rectangle((rect_top_left_coords, rect_bottom_right_coords), fill, stroke, stroke_width)
    img.show()
    return img

def draw_circle(img, pos_x, pos_y, diameter, fill, stroke, stroke_width):
    draw = ImageDraw.Draw(img)
    # https://note.nkmk.me/en/python-pillow-imagedraw/
    cir_top_left_coords = (pos_x, pos_y)
    cir_bottom_right_coords = (pos_x + diameter, pos_y + diameter)
    draw.ellipse((cir_top_left_coords, cir_bottom_right_coords), fill, stroke, stroke_width)
    img.show()
    return img

def draw_ellipse(img, cx, cy, rx, ry, fill, stroke, stroke_width):
    draw = ImageDraw.Draw(img)
    # https://note.nkmk.me/en/python-pillow-imagedraw/
    cir_top_left_coords = (cx, cy)
    cir_bottom_right_coords = (cx + rx, cy + ry)
    draw.ellipse((cir_top_left_coords, cir_bottom_right_coords), fill, stroke, stroke_width)
    img.show()
    return img


def draw_line(img, x1, y1, x2, y2, stroke, stroke_width):
    draw = ImageDraw.Draw(img)
    # https://note.nkmk.me/en/python-pillow-imagedraw/
    ln_top_left_coords = (x1, y1)
    ln_bottom_right_coords = (x2, y2)
    draw.line((ln_top_left_coords, ln_bottom_right_coords), stroke, stroke_width)
    img.show()
    return img


def draw_poly_line(img, coordinates, fill, stroke, stroke_width):
    draw = ImageDraw.Draw(img)

    # https://note.nkmk.me/en/python-pillow-imagedraw/
    for i in range(0, len(coordinates)):
        x1, y1 = coordinates[i]
        if i+1 != len(coordinates): 
            x2, y2 = coordinates[i+1]
            ln_top_left_coords = (x1, y1)
            ln_bottom_right_coords = (x2, y2)
            draw.line((ln_top_left_coords, ln_bottom_right_coords), stroke, stroke_width)
        #
    img.show()
    return img


# Parsing Rectangle - https://www.w3schools.com/graphics/svg_rect.asp
# Rectangle xpath selector = "//rect"
# Attributes to check:
#   width, height
#   x, y position
#   rx, ry


def parse_rectangle(img, element):
    rect_x = int(element.attrib.get("x"))
    rect_y = int(element.attrib.get("y"))
    rect_rx = element.attrib.get("rx")
    rect_ry = element.attrib.get("ry")
    rect_width = int(element.attrib.get("width"))
    rect_height = int(element.attrib.get("height"))

    fill, stroke, stroke_width = get_fill_outline(element)

    print(f"Fill: {fill}, Stroke color: {stroke}, Stroke width: {stroke_width}")

    print(f"X: {rect_x}, Y: {rect_y}")
    print(f"RX: {rect_rx}, RY: {rect_ry}")
    print(f"Width: {rect_width}, Height: {rect_height}")

    img = draw_rect_square(img, rect_x, rect_y, rect_width, rect_height, fill, stroke, stroke_width)
    img.save(FILE_NAME.replace(".svg", ".png"), 'PNG')
    return None

def parse_circle(img, element):
    cir_x = int(element.attrib.get("cx"))
    cir_y = int(element.attrib.get("cy"))
    radius = int(element.attrib.get("r"))
    diameter = radius * 2

    fill, stroke, stroke_width = get_fill_outline(element)

    print(f"Fill: {fill}, Stroke color: {stroke}, Stroke width: {stroke_width}")

    print(f"CX: {cir_x}, CY: {cir_y}")
    print(f"Radius: {radius}")

    img = draw_circle(img, cir_x, cir_y, diameter, fill, stroke, stroke_width)
    img.save(FILE_NAME.replace(".svg", ".png"), 'PNG')
    return None

def parse_ellipse(img, element):
    cx = int(element.attrib.get("cx"))
    cy = int(element.attrib.get("cy"))
    rx = int(element.attrib.get("rx"))
    ry = int(element.attrib.get("ry"))

    fill, stroke, stroke_width = get_fill_outline(element)

    print(f"Fill: {fill}, Stroke color: {stroke}, Stroke width: {stroke_width}")

    print(f"CX: {cx}, CY: {cy}")
    print(f"RX: {rx}, RY: {ry}")

    img = draw_ellipse(img, cx, cy, rx, ry, fill, stroke, stroke_width)
    img.save(FILE_NAME.replace(".svg", ".png"), 'PNG')
    return None

def parse_line(img, element):
    # <line x1="0" y1="0" x2="200" y2="200" style="stroke:rgb(255,0,0);stroke-width:2" />
    x1 = int(element.attrib.get("x1"))
    y1 = int(element.attrib.get("y1"))
    x2 = int(element.attrib.get("x2"))
    y2 = int(element.attrib.get("y2"))

    stroke, stroke_width = get_fill_lines(element)

    print(f"Stroke color: {stroke}, Stroke width: {stroke_width}")

    print(f"X1: {x1}, Y1: {y1}")
    print(f"X2: {x2}, Y2: {y2}")

    img = draw_line(img, x1, y1, x2, y2, stroke, stroke_width)
    img.save(FILE_NAME.replace(".svg", ".png"), 'PNG')
    return None
    

def parse_poly_line(img, element):
    # <polyline points="20,20 40,25 60,40 80,120 120,140 200,180"
    points = element.attrib.get("points")
    coordinates = []
    for point in points.split(" "):
        x_str, y_str = point.split(",")
        coordinates.append((int(x_str), int(y_str)))
    #
    print(f"Points: {points}")
    print(f"Coordinates: {coordinates}")

    fill, stroke, stroke_width = get_fill_outline(element)

    print(f"Fill: {fill}, Stroke color: {stroke}, Stroke width: {stroke_width}")

    img = draw_poly_line(img, coordinates, fill, stroke, stroke_width)
    img.save(FILE_NAME.replace(".svg", ".png"), 'PNG')
    return None

def detect_elm(img, element_tree):
    rect_element = element_tree.xpath("//rect")
    cir_element = element_tree.xpath("//circle")
    el_element = element_tree.xpath("//ellipse")
    ln_element = element_tree.xpath("//line")
    pol_ln_element = element_tree.xpath("//polyline")
    path_element = element_tree.xpath("//path")
    #
    if rect_element:
        print("Element is a rectangle!")
        parse_rectangle(img, rect_element[0])
        return rect_element[0]
    #
    elif cir_element:
        print("Element is a circle!")
        parse_circle(img, cir_element[0])
        return cir_element[0]
    #
    elif el_element:
        print("Element is a ellipse!")
        parse_ellipse(img, el_element[0])
        return el_element[0]
    #
    elif ln_element:
        print("Element is a line!")
        parse_line(img, ln_element[0])
        return ln_element[0]
    #
    elif pol_ln_element:
        print("Element is a polyline!")
        parse_poly_line(img, pol_ln_element[0])
        return pol_ln_element[0]
    #
    elif path_element:
        print("Element is a path!")
        parse_ellipse(img, path_element[0])
        return path_element[0]
    #
    else:
        print("Unknown element, not able to parse!")
    return None
        
def parse_svg(svg_tree, element):

    width = int(element.attrib.get("width"))
    height = int(element.attrib.get("height"))

    print(f"Width: {width}, Height: {height}")

    if width and height:
        img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    else:
        img = Image.new("RGBA", (IMAGE_WIDTH, IMAGE_HEIGHT), (255, 255, 255, 0))

    # EFF THIS SHIT WHY THE HECK AIN T YOU WORKING I M TIRED FML... MOST LIKELY SOME STUPID CRAP BUT WELL
    for child in svg_tree:
        print(child.tag, child.attrib)
        detect_elm(img, child)
    return None

svg_xml = open_svg(FILE_NAME)
svg_tree = lxml.html.fromstring(svg_xml)
svg_element = svg_tree.xpath("//svg")
if svg_element:
    print("Found SVG tag!")
    parse_svg(svg_tree, svg_element[0])

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
