# Contains all the draw functions
# https://note.nkmk.me/en/python-pillow-imagedraw/

from PIL import Image, ImageDraw
import box

class Picasso(object):
    def __init__(self, img_width, img_height):
        self.img_width = img_width
        self.img_height = img_height
        self.img_obj, self.draw_obj = self.draw_base()
        return None
    #
    def draw_base(self):
        img_obj = Image.new("RGBA", (self.img_width, self.img_height), (255, 255, 255, 0))
        draw_obj = ImageDraw.Draw(img_obj)
        return img_obj, draw_obj
    #
    # Rect or Square
    def draw_quadrilateral(self, data):
        top_left_coords = (data.x, data.y)
        bottom_right_coords = (data.x + data.width, data.y + data.height)
        self.draw_obj.rectangle((top_left_coords, bottom_right_coords), fill=data.fill, outline=data.stroke, width=data["stroke-width"])
        return None
    #
    # Draw circle/ellipse
    # Circle params - (x, y, diameter, diameter)
    # Ellipse params - (cx, cy, rx, ry)
    def draw_closed_curve(self, data):
        top_left_coords = (data.cx, data.cy)
        bottom_right_coords = (data.cx + data.rx, data.cy + data.ry)
        self.draw_obj.ellipse((top_left_coords, bottom_right_coords), fill=data.fill, outline=data.stroke, width=data["stroke-width"])
        return None
    #
    def draw_line(self, data):
        top_left_coords = (data.x1, data.y1)
        bottom_right_coords = (data.x2, data.y2)
        self.draw_obj.line((top_left_coords, bottom_right_coords), fill=data.stroke, width=data["stroke-width"])
        return None
    #
    def draw_poly_line(self, data):
        coordinates = data.coordinates
        for i in range(0, len(coordinates)):
            ln_data = box.Box({})
            ln_data.x1, ln_data.y1 = coordinates[i]
            if i+1 != len(coordinates): 
                ln_data.x2, ln_data.y2 = coordinates[i+1]
                self.draw_line(ln_data)
                # ln_top_left_coords = (x1, y1)
                # ln_bottom_right_coords = (x2, y2)
                # self.draw_obj.line((ln_top_left_coords, ln_bottom_right_coords), fill="green")
            #
        return None