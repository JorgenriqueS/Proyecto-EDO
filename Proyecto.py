# Se importa todas las librerías necesarias para la interfaz gráfica.
import sys
from tkinter import *
from tkinter import ttk
from tabulate import tabulate
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sympy import symbols, sympify
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Se crea la ventana principal para la interfaz gráfica.
pestaña1 = Tk()
pestaña1.resizable(1,1)
pestaña1.config(bg = "gray")
pestaña1.iconbitmap(".\galileo.ico")
pestaña1.title("Proyecto - Aplicaciones de EDO")

# Se crea dos subventanas para modificar la estética de la interfaz.
pestaña2 = Frame()
pestaña3 = Frame()

# Se configura la posición y color de cada subventana.
pestaña2.pack(fill = "x")
pestaña2.config(bg = "black")
pestaña2.config(width = "650", height = "60")
pestaña3.pack(fill = "y", side = "right")
pestaña3.config(width = "300", height = "650")

# Se crea textos para la interfaz gráfica, configurando color, letra, posición y el string.
txt_aut = Label(pestaña1, bg = "Gray", text = "Interfaz Gráfica implementada por: Diego Lezzer y Jorge Soto", font = ("Calibri bold", 16)).place(x = 250, y = 630)
txt_tit = Label(pestaña1, bg = "black", fg ="white", text = "Método de Runge-kutta", font = ("Calibri bold", 16)).place(x = 50, y = 10)
txt_IVI = Label(pestaña1, text = "Ingresar Valores Iniciales:", font = ("Calibri bold", 16)).place(x = 1115, y = 70)
txt_IVV = Label(pestaña1, text = "Ingresar Valores Variables:", font = ("Calibri bold", 16)).place(x = 1110, y = 210)
txt_opc = Label(pestaña1, text = "Seleccionar Aproximación:", font = ("Calibri bold", 16)).place(x = 1110, y = 350)
txt_fun = Label(pestaña1, bg = "Gray", text = "Ingresar Ecuación:", font = ("Calibri bold", 16)).place(x = 50, y = 80)
txt_x0 = Label(pestaña1, text = "X_0 =", font = ("Calibri bold", 16)).place(x = 1135, y = 120)
txt_y0 = Label(pestaña1, text = "Y_0 =", font = ("Calibri bold", 16)).place(x = 1135, y = 160)
txt_xn = Label(pestaña1, text = "X =", font = ("Calibri bold", 16)).place(x = 1145, y = 260)
txt_hn = Label(pestaña1, text = "H =", font = ("Calibri bold", 16)).place(x = 1145, y = 300)
txt_yp = Label(pestaña1, bg = "Gray", text = "Y'=", font = ("Calibri bold", 16)).place(x = 50, y = 120)

# Se crea espacios en blanco para ingresar datos.
entry_x0 = Entry(pestaña1)
entry_x0.place(x = 1190, y = 127)
entry_y0 = Entry(pestaña1)
entry_y0.place(x = 1190, y = 167)
entry_xn = Entry(pestaña1)
entry_xn.place(x = 1180, y = 267)
entry_hn = Entry(pestaña1)
entry_hn.place(x = 1180, y = 307)
entry_fu = Entry(pestaña1, width = 152)
entry_fu.place(x = 85, y = 127)

# Se crea un filtro con 3 posibles opciones de Aproximación Runge-Kutta 
select = IntVar()
select.set(3)
rk1 = Radiobutton(pestaña1, text = "Runge-Kutta orden 1", font = ("Calibri bold", 12), variable = select, value = 0).place(x = 1145, y = 400)
rk2 = Radiobutton(pestaña1, text = "Runge-Kutta orden 2", font = ("Calibri bold", 12), variable = select, value = 1).place(x = 1145, y = 440)
rk4 = Radiobutton(pestaña1, text = "Runge-Kutta orden 4", font = ("Calibri bold", 12), variable = select, value = 2).place(x = 1145, y = 480)

# Se crea la función calcular y un botón indicando que al presionarlo graficará y tabulará datos.
def calcular():
    x0 = int(entry_x0.get())
    y0 = int(entry_y0.get())
    xn = float(entry_xn.get())
    hn = float(entry_hn.get())
    fu = entry_fu.get()

    #llamando a todos los Runge-Kutta, me devuelven listas
    rk1 = RK1(fu, x0, y0, hn, xn)
    rk2 = RK2(fu, x0, y0, hn, xn)
    rk4 = RK4(fu, x0, y0, hn, xn)
    x = xOutput(x0, xn, hn)
    solucion = EDO(fu, y0, x)

    #mandando a graficar
    grafica(x, solucion, rk1, rk2, rk4, select.get())

bot_calcular = Button(pestaña1, text = "CALCULAR", command = calcular, bg = "white")
bot_calcular.place(x = 1145, y = 520)
bot_calcular.config(width = 22, height = 3)     

# Se crea la función cancelar y un botón indicando que al presionarlo cerrará la interfaz gráfica.
def cancelar():
    sys.exit()
bot_cancelar = Button(pestaña1, text = "CANCELAR", command = cancelar, bg = "white")
bot_cancelar.place(x = 1145, y = 600)
bot_cancelar.config(width = 22, height = 3)

# Se crea la tabla indicando la cantidad de columnas posibles y sus etiquetas.
tab = ttk.Treeview(pestaña1, columns = ("colum1", "colum2", "colum3", "colum4", "colum5"))
    
# Se crea las columnas de la tabla configurando el ancho y centrando los datos.
tab.column("#0", width = 70)
tab.column("colum1", width = 70, anchor = CENTER)
tab.column("colum2", width = 70, anchor = CENTER)
tab.column("colum3", width = 70, anchor = CENTER)
tab.column("colum4", width = 70, anchor = CENTER)
tab.column("colum5", width = 70, anchor = CENTER)
    
# Se crea textos especificando el nombre de cada columna centrándolo. 
tab.heading("#0", text = "X_n", anchor = CENTER)
tab.heading("colum1", text = "RK_1", anchor = CENTER)
tab.heading("colum2", text = "RK_2", anchor = CENTER)
tab.heading("colum3", text = "RK_4", anchor = CENTER)
tab.heading("colum4", text = "Var Real", anchor = CENTER)
tab.heading("colum5", text = "Error", anchor = CENTER)
    
# Se configura la tabla fijándola en una posición en específico.
tab.pack(side = LEFT)
tab.place(x = 50, y = 200)

# Se crea un apartado el cual realizará gráficas, configurando su tamaño y posición.
graf = Figure(figsize =(5, 4), dpi = 100)
fig = graf.add_subplot(111)
gen = FigureCanvasTkAgg(graf, master = pestaña1)
gen1 = gen.get_tk_widget()
gen1.pack()
gen1.place(x = 500, y = 200)

# Se crea la función gráfica asegurando que esté en blanco, indicando que habrán dos curvas, especificando ejes y dibujar dichas curvas.
def grafica(eje_x, listaReal, rk1, rk2, rk4, s):
    fig.clear()
    list = [rk1, rk2, rk4]
    p = ["1", "2", "4"]
    fig.plot(eje_x, listaReal, label='Real', color='blue', marker="o")
    fig.plot(eje_x, list[s], label='Aproximado', color='red',marker="o")
    fig.set_title('Solución exacta de la EDO vs Runge-Kutta orden ' + p[s])
    fig.set_xlabel('X')
    fig.set_ylabel('Y')
    fig.legend()
    gen.draw()

# Se agrega una imagen en la interfaz gráfica, configurando su posición y tamaño.
imagen = Image.open(".\logo2.png")  
imagen = imagen.resize((150, 50), Image.Resampling.LANCZOS)
im = ImageTk.PhotoImage(imagen)
imagen_label = Label(pestaña1, image = im).place(x = 1150, y = 3)
    
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

# Se crea la función Runge-Kutta orden 2 y la implementación de la misma.
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

# Funcion que genera todos los valores de x, ya que estos son independientes de cualquier Runge-Kutta
def xOutput(initial, final, step):
    puntos_x = []
    while(initial <= final):
        puntos_x.append(initial)
        initial += step
    return puntos_x

def EDO(string, y0, xArray):
    # Convertir el string en una función
    def ecuacion_diferencial(y, x):
        return eval(string)
        
    # Funcion de la libreria que resuelve la EDO
    solucion = odeint(ecuacion_diferencial, y0, xArray)
    return solucion

pestaña1.mainloop()
