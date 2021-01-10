"""
Intakes .svg file, renders as .png using strict libraries
no packages
XML parsing libaries, libraries writing png files are allowed

ONLY REQUIRED SVG IMPLEMENTATION: LINE, RECT, CIRC, ELLIPS, PATH, POLILYNE
INPUT: svg.py image.svg || OUTPUT: image.png
"""

#Initialize libraries
import sys
from xml.etree import ElementTree as ET


def main(svgFileInput):
    #Declare local variables
    svgFile = ET.parse(svgFileInput) #Parses the input svg image
    root =  svgFile.getroot() #Fetches the root XML tree from the svg file
    shapeType = [] #Stores the active shapes within the image
    shapeAttrib = [] #Stores the shapes attributes
    
    #Loop through the xml tree, assign shapes into array
    for child in root:
        for layerTree in child:
            for shape in layerTree:
                shapeType.append(shape.tag) #Identifies the type of shape
                shapeAttrib.append(shape.attrib) #Correlates shape data with identity from shapeType array

    #Prints current shapes within the svg picture
    for x in range(0, len(shapeType)):
        print("SHAPE TYPE: " + str(shapeType[x]) + "\nSHAPE ATTRIBUTE: " + str(shapeAttrib[x]))
        
    """
    #Trims the "excess" xml code off of the attributes
    for x in len(shapeAttrib):
    """
        
    """
    #create local variables
    img = [] #Array to construct the SVG input to PNG file writing export

    #handle creating the png image
    for y in range(IMG_HEIGHT):
        row = ()
        for x in range(IMG_WIDTH):
            
    #handle writing the  png file
    with open("image.png", img)
    """
    
if __name__ == "__main__":
    main(sys.argv[1])
