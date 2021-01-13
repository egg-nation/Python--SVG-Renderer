import box
import lxml.html
import sys
from picasso import Picasso
from pprint import pprint

FILE_NAME = sys.argv[-1]
print(FILE_NAME)

def open_svg(file):
    '''
    Opens the given input file "file" for reading,
    returns the read text

    :file: a string naming the file
    '''

    with open(file, "r") as input_fp:
        svg_xml = input_fp.read()

    return svg_xml

def get_attributes_data(element):
    '''
        Stores the data for the given element: attributes and their specific values, using Box

        :element: the node
    '''

    data = box.Box({})
    data.tag = element.tag
    data.element = element

    for k, v in element.attrib.items():
        print(k,v)

        if v.isnumeric():
            data[k] = int(v)
        else:
            data[k] = v

    data = get_styles(data)
    pprint(dict(data))
    return data

def parse_css_string(css_string, styles):
    '''
        Parses the in-line CSS so that we can get the data that we need from it: a propriety + its value,
        and then it adds it to the list of styles,
        returns the updates styles box

        :css_string: the string with the useful css to be parsed
        :styles: a box with the attributes
    '''

    props = css_string.split(";")

    for prop in props:
        prop_name, prop_value = prop.split(":")
        styles[prop_name] = prop_value

    return styles

def get_style_of_elm(element):
    '''
        Gets the values in the style attribute,
        and then it calls a function to parse it to get the data that we need from it,
        after getting the data, it returns it in the styles box

        :element: a node for a shape
    '''

    styles = box.Box({})
    css_string = element.attrib.get("style")

    if css_string:
        styles = parse_css_string(css_string, styles)

    return styles

def get_styles(data):
    '''
        Gets the stroke, stroke-width and fill from either in-line CSS or regular attributes,
        if there aren't any, it sets default values,
        returns the updated data

        :data: the box with attributes and their values
    '''

    styles = get_style_of_elm(data.element)
    if not styles:
        parent_element = data.element.getparent()
        print(f"This is parent")

        if parent_element.tag == "g":
            styles = get_style_of_elm(parent_element)

            if not styles.get("stroke"):
                styles.stroke = parent_element.attrib.get("stroke")

            if not styles.get("fill"):
                styles.fill = parent_element.attrib.get("fill")

            if not styles.get("stroke-width"):
                styles["stroke-width"] = parent_element.attrib.get("stroke-width")

    # setting default styles
    if not styles.get("stroke"):
        styles.stroke = "rgba(255,255,255,0)"

    if not styles.get("fill"):
        styles.fill = None

    if not styles.get("stroke-width"):
        styles["stroke-width"] = "5"

    # setting styles from inline css if no attributes are present
    if not data.get("stroke"):
        data.stroke = styles.stroke

    if not data.get("fill"):
        data.fill = styles.fill

    if not data.get("stroke-width"):
        data["stroke-width"] = styles["stroke-width"]

    # converting width to int
    data["stroke-width"] = int(data["stroke-width"])
    return data

def parse_rectangle(element):
    '''
            Gets the attributes needed to draw a rectable,
            returns the data

            :element: the rectangle node
   '''

    data = get_attributes_data(element)
    return data 

def parse_circle(element):
    '''
        Gets the attributes needed (diameter, which it ray*2) to draw a circle,
        returns the data

        :element: the circle node
    '''

    data = get_attributes_data(element)
    diameter = data.r * 2

    # for circle rx & ry is diamenter
    data.rx, data.ry = diameter, diameter
    return data

def parse_ellipse(element):
    '''
        Gets the attributes needed to draw an ellipse,
        returns the data

        :element: the ellipse node
    '''

    data = get_attributes_data(element)
    return data

def parse_line(element):
    '''
        Gets the attributes needed to draw a line,
        returns the data

        :element: the line node
    '''

    data = get_attributes_data(element)
    return data
    

def parse_poly_line(element):
    '''
        Gets the attributes needed to draw a polyline,
        saves the point coordinates inside data.coordinates
        returns the data

        :element: the polyline node
    '''

    data = get_attributes_data(element)

    points = data.points
    coordinates = []

    for point in points.split(" "):
        x_str, y_str = point.split(",")
        coordinates.append((int(x_str), int(y_str)))

    print(f"Points: {points}")
    print(f"Coordinates: {coordinates}")

    data.coordinates = coordinates
    return data


def parse_path(element):
    '''
        Gets SOME of the attributes needed (from the attribute d it gets M, L etc and finds the needed data values for each) to draw a path,
        returns the data
        IMPORTANT: It is the basic basic basic path, no complex stuff here, sorry

        :element: the path node
    '''

    data = get_attributes_data(element)
    coordinates = []

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
            if "M" in item:
                # Move to
                initial_x = int(item.strip("M"))
                initial_y = int(data_items.pop(0))
                coordinates.append((initial_x, initial_y))

            elif "L" in item:
                cursor_x = int(item.strip("L"))
                cursor_y = int(data_items.pop(0))
                coordinates.append((cursor_x, cursor_y))

            elif "Z" in item:
                # closing Path, drawing line to initial point
                coordinates.append((initial_x, initial_y))
        #
        else:
            if "M" == item:
                # Move to
                initial_x = int(data_items.pop(0))
                initial_y = int(data_items.pop(0))
                coordinates.append((initial_x, initial_y))

            elif "L" == item:
                cursor_x = int(data_items.pop(0))
                cursor_y = int(data_items.pop(0))
                coordinates.append((cursor_x, cursor_y))

            elif "Z" == item:
                # closing Path, drawing line to initial point
                coordinates.append((initial_x, initial_y))

    print(f"Path Data: {path_data}")
    print(coordinates)

    data.coordinates = coordinates
    return data


def detect_elm(svg_tree):
    '''
        Detects tags in the given XML tree to go further with drawing specific shapes according to the attributes of the mentioned tags
        - First, it selects the SVG node from the XML tree to get the height and width attributes in case they are specified,
          otherwise, it goes with a 1920*1080 to avoid complications for the path and other "questionable" shapes
          (it would be easy to find them for rect, ellipse, circle etc) => calls function to draw the background
        - Next, it selects the following SVG nodes for groups and the specified shapes and for each element found it parses it to get the data needed for drawing it:
          RECTANGLE, CIRCLE, ELLIPSE, PATH, LINE, POLYLINE OR A GROUP WHICH CONTAINS THEM
        - Finally, it shows and saved the obtained image

        :svg_tree: the XML tree
    '''

    svg_elm = svg_tree.xpath("//svg")[0]
    img_width, img_height = 1920, 1080

    if svg_elm.attrib.get("width"):
        img_width = int(svg_elm.attrib.get("width"))

    if svg_elm.attrib.get("height"):
        img_height = int(svg_elm.attrib.get("height"))

    print(f"Image Width: {img_width} & Image Height: {img_height}")
    picasso_obj = Picasso(img_width, img_height)

    svg_elements = svg_tree.xpath(".//*[not(name()='g')]")

    for element in svg_elements:
        if element.tag == "rect":
            print("Element is a rectangle!")
            data = parse_rectangle(element)
            picasso_obj.draw_quadrilateral(data)

        elif element.tag == "circle":
            print("Element is a circle!")
            data = parse_circle(element)
            picasso_obj.draw_closed_curve(data)

        elif element.tag == "ellipse":
            data = parse_ellipse(element)
            picasso_obj.draw_closed_curve(data)

        elif element.tag == "line":
            print("Element is a line!")
            data = parse_line(element)
            picasso_obj.draw_line(data)

        elif element.tag == "polyline":
            print("Element is a polyline!")
            data = parse_poly_line(element)
            picasso_obj.draw_poly_line(data)

        elif element.tag == "path":
            print("Element is a path!")
            data = parse_path(element)
            picasso_obj.draw_poly_line(data)

        else:
            print("Unknown element, not able to parse!")

    picasso_obj.img_obj.show()
    picasso_obj.img_obj.save(FILE_NAME.replace(".svg", ".png"))
    return None
        

svg_xml = open_svg(FILE_NAME)

'''
    Transform the string obtained from reading the file into an easy to parse XML

    :svg_tree: the XML tree
'''
svg_tree = lxml.html.fromstring(svg_xml)
detect_elm(svg_tree)