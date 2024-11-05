from sympy import *

x, y, m, c = symbols("x y m c")
x_1, y_1, x_2, y_2 = symbols("x_1 y_1 x_2 y_2")

formulas = {}
formulas[y] = m*x + c
formulas[m] = (y_2 - y_1)/(x_2 - x_1)
formulas[y - y_1] = m * (x - x_1)
formulas[(y - y_1) / (y_2 - y_1)] = (x - x_1) / (x_2 - x_1)
