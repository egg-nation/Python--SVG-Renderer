import lxml.html
# import turtle
from picasso import Picasso
import box
from pprint import pprint
import sys

# Get height and width from svg file.
# Check if bg needs to be transparent.
# IMAGE_WIDTH = 1000
# IMAGE_HEIGHT = 500
# FILE_NAME = "rect.svg"
# FILE_NAME = "cir.svg"
# FILE_NAME = "el.svg"
# FILE_NAME = "ln.svg"
# FILE_NAME = "poly_ln.svg"
# FILE_NAME = "path1.svg"
# FILE_NAME = "combined.svg"


FILE_NAME = sys.argv[-1]
print(FILE_NAME)


def open_svg(file):
    with open(file, "r") as input_fp:
        svg_xml = input_fp.read()
    return svg_xml


# Parsing Rectangle - https://www.w3schools.com/graphics/svg_rect.asp
# Rectangle xpath selector = "//rect"
# Attributes to check:
#   width, height
#   x, y position
#   rx, ry

def get_attributes_data(element):
    data = box.Box({})
    data.tag = element.tag
    for k, v in element.attrib.items():
        print(k, v)
        if v.isnumeric():
            data[k] = int(v)
        else:
            data[k] = v
    #
    data = parse_css(data)
    pprint(dict(data))
    return data


def parse_inline_styles(css_string):
    # style="stroke:rgb(255,0,0);stroke-width:2"
    styles = box.Box({
        # default styles
        "stroke": "rgb(255,0,0)",
        "fill": "none",
        "stroke-width": "5"
    })
    if css_string:
        props = css_string.split(";")
        for prop in props:
            prop_name, prop_value = prop.split(":")
            styles[prop_name] = prop_value
    return styles


def parse_css(data):
    css_string = data.get("style")
    styles = parse_inline_styles(css_string)
    #
    if not data.get("stroke"):
        data.stroke = styles.stroke
    if not data.get("fill"):
        data.fill = styles.fill
    if not data.get("stroke-width"):
        data["stroke-width"] = int(styles["stroke-width"])
    #
    # convert width to int
    data["stroke-width"] = int(data["stroke-width"])
    return data


def parse_rectangle(element):
    data = get_attributes_data(element)
    return data


def parse_circle(element):
    data = get_attributes_data(element)
    diameter = data.r * 2
    # For circle rx & ry is diamenter
    data.rx, data.ry = diameter, diameter
    return data


def parse_ellipse(element):
    data = get_attributes_data(element)
    return data


def parse_line(element):
    data = get_attributes_data(element)
    return data


def parse_poly_line(element):
    data = get_attributes_data(element)
    # <polyline points="20,20 40,25 60,40 80,120 120,140 200,180"
    points = data.points
    coordinates = []
    for point in points.split(" "):
        x_str, y_str = point.split(",")
        coordinates.append((int(x_str), int(y_str)))
    #
    print(f"Points: {points}")
    print(f"Coordinates: {coordinates}")

    data.coordinates = coordinates
    return data


def parse_path(element, draw_obj):
    path_data = element.attrib.get("d")
    data_items = path_data.split(" ")
    initial_x, cursor_x = 0, 0
    initial_y, cursor_y = 0, 0
    while data_items:
        item = data_items.pop(0).upper()
        print(f"Item: {item}")
        print(f"Init_x: {initial_x}, Init_y: {initial_y}")
        print(f"Cur_x: {cursor_x}, Cur_y: {cursor_y}")
        if len(item) > 1:
            # M150
            if "M" in item:
                # Move to
                initial_x = int(item.strip("M"))
                initial_y = int(data_items.pop(0))
                # #
                # initial_x = cursor_x
                # initial_y = cursor_y
            elif "L" in item:
                cursor_x = int(item.strip("L"))
                cursor_y = int(data_items.pop(0))
                draw_obj = draw_line(initial_x, initial_y, cursor_x, cursor_y, draw_obj)
            elif "Z" in item:
                # Close Path, draw line to initial point
                draw_obj = draw_line(cursor_x, cursor_y, initial_x, initial_y, draw_obj)
        #
        else:
            # M150
            if "M" == item:
                # Move to
                initial_x = int(data_items.pop(0))
                initial_y = int(data_items.pop(0))
                # #
                # initial_x = cursor_x
                # initial_y = cursor_y
            elif "L" == item:
                cursor_x = int(data_items.pop(0))
                cursor_y = int(data_items.pop(0))
                draw_obj = draw_line(initial_x, initial_y, cursor_x, cursor_y, draw_obj)
            elif "Z" == item:
                # Close Path, draw line to initial point
                draw_obj = draw_line(initial_x, initial_y, cursor_x, cursor_y, draw_obj)
                # draw_obj = draw_line(cursor_x, cursor_y, initial_x, initial_y, draw_obj)

    print(f"Path Data: {path_data}")
    # draw_obj = draw_ellipse(cx, cy, rx, ry, draw_obj)
    # img.save(FILE_NAME.replace(".svg", ".png"))
    return draw_obj


def detect_elm(svg_tree):
    svg_elm = svg_tree.xpath("//svg")[0]
    img_width, img_height = 1920, 1080
    if svg_elm.attrib.get("width"):
        img_width = int(svg_elm.attrib.get("width"))
    #
    if svg_elm.attrib.get("height"):
        img_height = int(svg_elm.attrib.get("height"))
    #
    print(f"Image Width: {img_width} & Image Height: {img_height}")
    picasso_obj = Picasso(img_width, img_height)
    #
    svg_elements = svg_tree.getchildren()
    for element in svg_elements:
        if element.tag == "rect":
            print("Element is a rectangle!")
            data = parse_rectangle(element)
            picasso_obj.draw_quadrilateral(data)
        #
        elif element.tag == "circle":
            print("Element is a circle!")
            data = parse_circle(element)
            picasso_obj.draw_closed_curve(data)
        #
        elif element.tag == "ellipse":
            data = parse_ellipse(element)
            picasso_obj.draw_closed_curve(data)
        #
        elif element.tag == "line":
            print("Element is a line!")
            data = parse_line(element)
            picasso_obj.draw_line(data)
        #
        elif element.tag == "polyline":
            print("Element is a polyline!")
            data = parse_poly_line(element)
            picasso_obj.draw_poly_line(data)
        #
        elif element.tag == "path":
            print("Element is a path!")
            draw_obj = parse_path(element)
        #
        else:
            print("Unknown element, not able to parse!")
    #
    picasso_obj.img_obj.show()
    picasso_obj.img_obj.save(FILE_NAME.replace(".svg", ".png"))
    return None


svg_xml = open_svg(FILE_NAME)
svg_tree = lxml.html.fromstring(svg_xml)
detect_elm(svg_tree)