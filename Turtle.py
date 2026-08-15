import turtle

t = turtle.Turtle("circle")
t.speed(67)
led = ['red', 'green', 'blue']

for i in range(0,300,2):
    t.color(led[i%len(led)])
    t.left(90)
    t.forward(20 + i)
    