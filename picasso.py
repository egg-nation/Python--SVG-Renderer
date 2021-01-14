# Contains all the draw functions
# https://note.nkmk.me/en/python-pillow-imagedraw/

from PIL import Image, ImageDraw
import box
from aggdraw import Draw, Path

#stackoverflow https://stackoverflow.com/questions/246525/how-can-i-draw-a-bezier-curve-using-pythons-pil
def make_bezier(xys):
    '''
        Returns
        http://en.wikipedia.org/wiki/B%C3%A9zier_curve#Generalization

        :xys: sequence of Bezier control points given as 2-tuples
    '''
    # xys should be a sequence of 2-tuples (Bezier control points)
    n = len(xys)
    combinations = pascal_row(n - 1)

    def bezier(ts):
        # This uses the generalized formula for bezier curves
        # http://en.wikipedia.org/wiki/B%C3%A9zier_curve#Generalization
        result = []
        for t in ts:
            tpowers = (t ** i for i in range(n))
            upowers = reversed([(1 - t) ** i for i in range(n)])
            coefs = [c * a * b for c, a, b in zip(combinations, tpowers, upowers)]
            result.append(
                tuple(sum([coef * p for coef, p in zip(coefs, ps)]) for ps in zip(*xys)))
        return result

    return bezier

#stackoverflow
def pascal_row(n, memo={}):
    # This returns the nth row of Pascal's Triangle
    if n in memo:
        return memo[n]
    result = [1]
    x, numerator = 1, n
    for denominator in range(1, n // 2 + 1):
        # print(numerator,denominator,x)
        x *= numerator
        x /= denominator
        result.append(x)
        numerator -= 1
    if n & 1 == 0:
        # n is even
        result.extend(reversed(result[:-1]))
    else:
        result.extend(reversed(result))
    memo[n] = result
    return result

class Picasso(object):
    def __init__(self, img_width, img_height):
        '''
            Initialization

            :self: the object
            :img_width: the width of the SVG background
            :img_height: the height of the SVG background
        '''
        self.img_width = img_width
        self.img_height = img_height
        self.img_obj, self.draw_obj = self.draw_base()
        return None

    def draw_base(self):
        '''
            Initializez the img_obj (the transparent background for the svg) and draw_obj (by now only the base),
            draws the background
            returns them

            :self: the object
        '''
        img_obj =  Image.new("RGBA", (self.img_width, self.img_height), (255, 255, 255, 0))
        draw_obj = ImageDraw.Draw(img_obj)
        return img_obj, draw_obj

    def draw_quadrilateral(self, data):
        '''
            Used for drawing the rectangle or square according to the attribute values stored in the data box
            - Rectangle/Square parameters - (x, y, x + width, y + width)

            :self: the object
            :data: the box with attributes and their values
        '''
        top_left_coords = (data.x, data.y)
        bottom_right_coords = (data.x + data.width, data.y + data.height)
        self.draw_obj.rectangle((top_left_coords, bottom_right_coords), fill=data.fill, outline=data.stroke,
                                width=data["stroke-width"])
        return None

    def draw_closed_curve(self, data):
        '''
            Used for drawing ellipse and circle according to the attributes and values stored in the data box
            - Circle parameters - (x, y, diameter, diameter)
            - Ellipse parameters - (cx, cy, rx, ry)

            :self: the object
            :data: the box with attributes and their values
        '''
        top_left_coords = (data.cx, data.cy)
        bottom_right_coords = (data.cx + data.rx, data.cy + data.ry)
        self.draw_obj.ellipse((top_left_coords, bottom_right_coords), fill=data.fill, outline=data.stroke,
                              width=data["stroke-width"])
        return None
    #
    def draw_line(self, data):
        '''
            Used for drawing the line according to the attributes and values stored in the data box
            - Line - (x1, y1, x2, y2)

            :self: the object
            :data: the box with attributes and their values
        '''
        top_left_coords = (data.x1, data.y1)
        bottom_right_coords = (data.x2, data.y2)
        self.draw_obj.line((top_left_coords, bottom_right_coords), fill=data.stroke, width=data["stroke-width"])
        return None
    #
    def draw_poly_line(self, data):
        '''
            Used for drawing the polyline according to the attributes and values stored in the data box
            - It draws multiple lines according to the list of coordinates - (xi, yi, xj, yj)

            :self: the object
            :data: the box with attributes and their values
        '''
        coordinates = data.coordinates
        for i in range(0, len(coordinates)):
            ln_data = box.Box({})
            ln_data.stroke = data.stroke
            ln_data.fill = data.fill
            ln_data["stroke-width"] = data["stroke-width"]
            ln_data.x1, ln_data.y1 = coordinates[i]
            if i + 1 != len(coordinates):
                ln_data.x2, ln_data.y2 = coordinates[i + 1]
                self.draw_line(ln_data)
        return None

    def draw_path(self, data):
        coordinates = data.coordinates
        coordinates_bezier_control_points = data.coordinates_bezier_control_points
        coordinates_bezier_end_points = data.coordinates_bezier_end_points
        ts = [t / 100.0 for t in range(101)]

        points = []
        #points = coordinates
        bezier_points = coordinates_bezier_control_points
        bezier_points.extend(coordinates_bezier_end_points)
        xys = bezier_points
        bezier = make_bezier(xys)
        points.extend(bezier(ts))



        # xys = [(50, 100), (80, 80), (100, 50)]
        # bezier = make_bezier(xys)
        # points = bezier(ts)
        #u
        # xys = [(100, 50), (100, 0), (50, 0), (50, 35)]
        # bezier = make_bezier(xys)
        # points.extend(bezier(ts))
        # c
        # xys = [(50, 35), (50, 0), (0, 0), (0, 50)]
        # bezier = make_bezier(xys)
        # points.extend(bezier(ts))
        #
        # xys = [(0, 50), (20, 80), (50, 100)]
        # bezier = make_bezier(xys)
        # points.extend(bezier(ts))
        # #points.extend(coordinates)

        self.draw_obj.polygon(points,  fill=data.fill, outline=data.stroke)
        return None
