# Contains all the draw functions
# https://note.nkmk.me/en/python-pillow-imagedraw/

from PIL import Image, ImageDraw
import box

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