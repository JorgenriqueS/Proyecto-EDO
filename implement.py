from sympy import symbols, sympify
from tabulate import tabulate
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import numpy as np

def EDO(string, y0, xArray):
    # Convertir el string en una función
    def ecuacion_diferencial(y, x):
        return eval(string)
        
    # Funcion de la libreria que resuelve la EDO
    solucion = odeint(ecuacion_diferencial, y0, xArray)
    return solucion

def graficar(eje_x, real, rk1, rk2, rk4, i):
    if (i == 1): 
        k = 0
    if (i == 2): 
        k = 1
    if (i == 4): 
        k = 2

    # Graficar la solución
    l = [rk1, rk2, rk4]
    p = ["1", "2", "4"]
    plt.figure(figsize=(8, 6))
    plt.plot(eje_x, real, label='solucion exacta', color='blue', marker="o")
    plt.plot(eje_x, l[k], label='solucion aproximada', color='red', marker="o")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.title('Solución exacta de la EDO vs Runge-Kutta orden '+p[k])
    plt.grid(True)
    plt.show()

def Function(string, x_valor, y_valor):
    x, y = symbols('x y') # Definir los símbolos que se utilizarán en la expresión
    expresion_sympy = sympify(string) # Convertir el string en una expresión sympy
    return expresion_sympy.subs([(x, x_valor), (y, y_valor)])

# Se crea la función Runge-Kutta orden 1 y la implementación de la misma.
def RK1(expr, x_0, y_0, step, final_val): 
    puntos_y = []

    while(x_0 <= final_val):
        puntos_y.append(y_0)
        f = Function(expr, x_0, y_0)
        y_0 += step*f
        x_0 += step

    return puntos_y

def RK2(expr, x_0, y_0, step, final_val):
    puntos_y = []

    while(x_0 <= final_val):
        puntos_y.append(y_0)
        k1 = Function(expr, x_0, y_0)   
        k2 = Function(expr, x_0 + step, y_0+(step*k1))
        y_0 = y_0 + ((step/2)*(k1+k2))
        x_0 += step
    return puntos_y

# Se crea la función Runge-Kutta orden 4 y la implementación de la misma.
def RK4(expr, x_0, y_0, step, final_val):
    puntos_y = []

    while(x_0 <= final_val):
        puntos_y.append(y_0)
        f = Function(expr, x_0, y_0)
        k1 = step*f
        f1 = Function(expr, x_0+(step/2), y_0+(k1/2))
        k2 = step*f1
        f2 = Function(expr, x_0+(step/2), y_0+(k2/2))
        k3 = step*f2
        f3 = Function(expr, x_0+step, y_0+k3)
        k4 = step*f3
        y_0 = y_0 +(1/6)*(k1+2*k2+2*k3+k4)
        x_0 += step
        
    return puntos_y

def xOutput(initial, final, step):
    puntos_x = []
    while(initial <= final):
        puntos_x.append(initial)
        initial += step
    return puntos_x

def main():
    #obteniendo parametros necesarios
    expr = input("Ingrese expresion: y´= ")
    x_0 = int(input("Ingrese valor inicial de x: "))
    y_0 = int(input("Ingrese valor inicial de y: "))
    x_f = float(input("Ingrese valor de x a calcular: "))
    h = float(input("Ingrese el valor del paso: "))
    t = int(input("Ingrese el orden de Runge-Kutta deseado: "))

    #mandando a llamar funciones para realizar aproximación con Runge-Kutta
    rk1 = RK1(expr, x_0, y_0, h, x_f)
    rk2 = RK2(expr, x_0, y_0, h, x_f)
    rk4 = RK4(expr, x_0, y_0, h, x_f)
    x = xOutput(x_0, x_f, h)
    exact = EDO(expr, y_0, x)

    print("Resultados del algoritmo para y'="+expr)
    print("----------------------------------------------------------------------------------")
    print(tabulate({"X_k": x, "RK1": rk1, "RK2": rk2, "RK4": rk4}, headers="keys", tablefmt="grid", colalign=["center", "center", "center", "center"]))
    graficar(x, exact, rk1, rk2, rk4, t)

main()




