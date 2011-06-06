
import turtle             # allows us to use turtles
wn = turtle.Screen()      # creates a playground for turtles
alex = turtle.Turtle()    # create a turtle, assign to alex

alex.forward(50)          # tell alex to move forward by 50 units
alex.left(90)             # tell alex to turn by 90 degrees
alex.forward(30)          # complete the second side of a rectangle

wn.mainloop()             # Leave the window active, until the user closes it