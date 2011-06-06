import turtle
wn = turtle.Screen()
wn.bgcolor("lightgreen")      # set the window background colour
wn.title("Hello, Tess!")      # set the window title

tess = turtle.Turtle()
tess.color("blue")            # tell tess to change her color
tess.pensize(3)               # tell tess to set the width of her pen

tess.forward(50)
tess.left(120)
tess.forward(50)

wn.mainloop()