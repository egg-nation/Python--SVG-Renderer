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
FILE_NAME = "group.svg"



FILE_NAME = sys.argv[-1]
print(FILE_NAME)
# FILE_NAME = "group.svg"

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
    data.element = element
    for k, v in element.attrib.items():
        print(k,v)
        if v.isnumeric():
            data[k] = int(v)
        else:
            data[k] = v
    #
    data = get_styles(data)
    pprint(dict(data))
    return data



def parse_css_string(css_string, styles):
    props = css_string.split(";")
    for prop in props:
        prop_name, prop_value = prop.split(":")
        styles[prop_name] = prop_value    
    return styles

def get_style_of_elm(element):
    styles = box.Box({})
    css_string = element.attrib.get("style")
    if css_string:
        styles = parse_css_string(css_string, styles)
    return styles

def get_styles(data):
    # 
    styles = get_style_of_elm(data.element)
    if not styles:
        parent_element = data.element.getparent()
        if parent_element.tag == "g":
            styles = get_style_of_elm(parent_element)
    #
    # set default styles
    if not styles.get("stroke"):
        styles.stroke = "rgb(255,0,0)"
    if not styles.get("fill"):
        styles.fill = None
    if not styles.get("stroke-width"):
        styles["stroke-width"] = "5"
    #
    # Set styles from inline css if no attributes present
    if not data.get("stroke"):
        data.stroke = styles.stroke
    if not data.get("fill"):
        data.fill = styles.fill
    if not data.get("stroke-width"):
        data["stroke-width"] = styles["stroke-width"]
    # 
    # convert width to int
    data["stroke-width"] = int(data["stroke-width"])
    return data

# def parse_css(data):
#     css_string = data.get("style")
#     styles = get_styles(css_string)
#     #
#     if not data.get("stroke"):
#         data.stroke = styles.stroke
#     if not data.get("fill"):
#         data.fill = styles.fill
#     if not data.get("stroke-width"):
#         data["stroke-width"] = int(styles["stroke-width"])
#     # 
#     # convert width to int
#     data["stroke-width"] = int(data["stroke-width"])
#     return data


    


def get_css(data):
    inline_css_str = data.get("style")
    if not inline_css_str:
        # Check for group style
        group_element = data.element.parent("//g")
        if group_element:
            group_styles

# Check for inline style
    #  if present get styles from that
    # if not check if it has parent element



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


def parse_path(element):
    data = get_attributes_data(element)
    coordinates = []
    #     
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
                coordinates.append((initial_x, initial_y))
                # # 
            elif "L" in item:
                cursor_x = int(item.strip("L"))
                cursor_y = int(data_items.pop(0))
                coordinates.append((cursor_x, cursor_y))
            elif "Z" in item:
                # Close Path, draw line to initial point
                coordinates.append((initial_x, initial_y))
        #
        else:
            # M150
            if "M" == item:
                # Move to
                initial_x = int(data_items.pop(0))
                initial_y = int(data_items.pop(0))
                coordinates.append((initial_x, initial_y))
                # # 
            elif "L" == item:
                cursor_x = int(data_items.pop(0))
                cursor_y = int(data_items.pop(0))
                coordinates.append((cursor_x, cursor_y))                
            elif "Z" == item:
                # Close Path, draw line to initial point
                coordinates.append((initial_x, initial_y))

    print(f"Path Data: {path_data}")
    print(coordinates)
    data.coordinates = coordinates
    return data


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
    # svg_elements = svg_tree.getchildren()
    svg_elements = svg_tree.xpath(".//*[not(name()='g')]")
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
            data = parse_path(element)
            picasso_obj.draw_poly_line(data)
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