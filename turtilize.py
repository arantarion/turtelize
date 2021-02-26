import sys
import turtle
import numpy as np
from PIL import Image
from turtle import Screen

###########################################################################################################
#                                   Setup and global configuration                                        #  
###########################################################################################################

try:
    IMAGE = sys.argv[1]
except:
    print("Please specify an image!")
    exit(-1)
RESIZE_FACTOR = 6
SCREEN_WIDTH = 1900
SCREEN_HEIGHT = 1000
POINT_DISTANCE = 3
TURTLE_SHAPE = "circle"  # ["arrow", "turtle", "circle", "square", "triangle", "classic"]
STAMP_MODE = False
TURTLE_SIZE = (0.1, 0.1, 0.1)
OUTPUT_NAME = "output.eps"

###########################################################################################################
#                                   Loading image and conversion to b/w                                   # 
###########################################################################################################

image_file = Image.open(IMAGE) 

width, height = image_file.size  
image_file = image_file.resize((width//RESIZE_FACTOR, height//RESIZE_FACTOR))   # resize by factor

image_file = image_file.convert('1')       # convert to black and white only
mat = np.asarray(image_file.convert('L'))  # matrix repr
mat_norm = np.where(mat==255, 1, mat)      # replace 255 (black) with 1 for fun
num_rows, num_cols = mat_norm.shape

###########################################################################################################
#                                   Decide color of graphic                                               #  
###########################################################################################################

color = 1 if len(np.flatnonzero(mat_norm)) >= num_cols*num_cols - len(np.flatnonzero(mat_norm)) else 0

###########################################################################################################
#                                   Configure turtle and screen                                           #  
###########################################################################################################

turtle.tracer(0, 0)
pen = turtle.Turtle(visible=False, shape=TURTLE_SHAPE)
pen.speed('fastest')
pen.resizemode("user")
pen.shapesize(*TURTLE_SIZE)

screen = Screen()
screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)

###########################################################################################################
#                                           Drawing function                                              #  
###########################################################################################################

def draw(space, num_rows, num_cols, pic): 
    for i in range(num_rows): 
        for j in range(num_cols):
            if pic[i, j] == 0: #color
                if STAMP_MODE:
                    pen.stamp()
                else:
                    pen.dot()
            pen.forward(space)

        pen.backward(space*num_cols) 
        pen.right(90) 
        pen.forward(space) 
        pen.left(90) 

    print(f"""No. of points: {num_cols*num_rows}
    No. of dots: {len(np.flatnonzero(pic))}
    No. of blanks: {num_cols*num_rows - len(np.flatnonzero(pic))}""")


###########################################################################################################
#                                           Main function                                                 #  
###########################################################################################################


pen.penup()
pen.goto(-940, 480)
draw(POINT_DISTANCE, num_rows, num_cols, mat_norm) 
pen.hideturtle()

turtle.update()

#ts = turtle.getscreen()
#ts.getcanvas().postscript(file=OUTPUT_NAME)

turtle.mainloop()