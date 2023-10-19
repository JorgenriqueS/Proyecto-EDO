import sys
from tkinter import *
from tkinter import ttk
from tabulate import tabulate
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def main():
    #graf, var = plt.subplots(dpi = 90, figsize = (7, 5))
    #plt.title("Gráfica de Aproximación Runge-Kutta", color = "black", size = 16, family = "Arial")
    #var.set_facecolor("gray")
    #var.axvline(linewidth = 2, color = "black")
    #var.axhline(linewidth = 2, color = "black")
    #var.set_xlabel("Eje Horizontal", color = "black")
    #var.set_ylabel("Eje Vertical", color = "black")
    #var.tick_params(direction = "out", length = 6, width = 2, color = "black", grid_color = "red", grid_alpha = 0.5)

    pestaña1 = Tk()
    pestaña1.resizable(1,1)
    pestaña1.config(bg = "gray")
    pestaña1.title("Proyecto - Aplicaciones de EDO")
    pestaña2 = Frame()
    pestaña3 = Frame()
    pestaña2.pack(fill = "x")
    pestaña3.pack(fill = "y", side = "right")
    pestaña2.config(bg = "black")
    pestaña2.config(width = "650", height = "60")
    pestaña3.config(width = "300", height = "650")
    texto1 = Label(pestaña1, bg = "black", fg ="white", text = "Método de Runge-kutta", font = ("Calibri", 16)).place(x = 10, y = 10)
    texto2 = Label(pestaña1, text = "Ingresar Valores Iniciales:", font = ("Calibri", 16)).place(x = 1115, y = 70)
    texto3 = Label(pestaña1, text = "X_0 =", font = ("Calibri", 16)).place(x = 1135, y = 120)
    cuadr1 = Entry(pestaña1).place(x = 1190, y = 127)
    texto4 = Label(pestaña1, text = "Y_0 =", font = ("Calibri", 16)).place(x = 1135, y = 160)
    cuadr2 = Entry(pestaña1).place(x = 1190, y = 167)
    texto5 = Label(pestaña1, text = "Ingresar Valores Variables:", font = ("Calibri", 16)).place(x = 1110, y = 210)
    texto6 = Label(pestaña1, text = "X =", font = ("Calibri", 16)).place(x = 1145, y = 260)
    cuadr3 = Entry(pestaña1).place(x = 1180, y = 267)
    texto7 = Label(pestaña1, text = "H =", font = ("Calibri", 16)).place(x = 1145, y = 300)
    cuadr4 = Entry(pestaña1).place(x = 1180, y = 307)
    texto8 = Label(pestaña1, text = "Seleccionar Aproximación:", font = ("Calibri", 16)).place(x = 1110, y = 350)

    select = IntVar()
    select.set(3)
    opcion1 = Radiobutton(pestaña1, text = "Runge-Kutta orden 1", font = ("Calibri", 12), variable = select, value = 1).place(x = 1145, y = 400)
    opcion2 = Radiobutton(pestaña1, text = "Runge-Kutta orden 2", font = ("Calibri", 12), variable = select, value = 2).place(x = 1145, y = 440)
    opcion3 = Radiobutton(pestaña1, text = "Runge-Kutta orden 4", font = ("Calibri", 12), variable = select, value = 3).place(x = 1145, y = 480)
    
    def aceptar():
        pass
    botons1 = Button(pestaña1, text = "ACEPTAR", command = aceptar, bg = "white")
    botons1.place(x = 1145, y = 520)
    botons1.config(width = 22, height = 3)
    
    def cancelar():
        sys.exit()
    botons2 = Button(pestaña1, text = "CANCELAR", command = cancelar, bg = "white")
    botons2.place(x = 1145, y = 600)
    botons2.config(width = 22, height = 3)
    
    tab = ttk.Treeview(pestaña1, columns = ("colum1", "colum2", "colum3", "colum4", "colum5"))
    
    tab.column("#0", width = 70)
    tab.column("colum1", width = 70, anchor = CENTER)
    tab.column("colum2", width = 70, anchor = CENTER)
    tab.column("colum3", width = 70, anchor = CENTER)
    tab.column("colum4", width = 70, anchor = CENTER)
    tab.column("colum5", width = 70, anchor = CENTER)
    
    tab.heading("#0", text = "X_n", anchor = CENTER)
    tab.heading("colum1", text = "RK_1", anchor = CENTER)
    tab.heading("colum2", text = "RK_2", anchor = CENTER)
    tab.heading("colum3", text = "RK_4", anchor = CENTER)
    tab.heading("colum4", text = "Var Real", anchor = CENTER)
    tab.heading("colum5", text = "Error", anchor = CENTER)
    tab.pack()
    tab.place(x = 50, y = 200)
    
    #frame = Frame(pestaña1, bg = "white", bd = 3)
    #frame.grid(column = 0, row = 0)
    
    #canvas = FigureCanvasTkAgg(graf, master = frame)
    #canvas.get_tk_widget().grid(column = 0, row = 0, columnspan = 3, padx = 5, pady = 5)

    pestaña1.mainloop()

def RK1(x_0, y_0, step, final_val): 
    puntos_x = [x_0]
    puntos_y = [y_0]

    while(x_0 <= final_val):
        f = func([x_0, y_0])
        y_0 += step*f
        x_0 += step
        puntos_x.append(x_0)
        puntos_y.append(y_0)

    return [puntos_x, puntos_y]

def RK4(x_0, y_0, step, final_val):
    puntos_x = [x_0]
    puntos_y = [y_0]

    while(x_0 <= final_val):
        f = func([x_0, y_0])
        k1 = step*f
        f1 = func([x_0+(step/2), y_0+(k1/2)])
        k2 = step*f1
        f2 = func([x_0+(step/2), y_0+(k2/2)])
        k3 = step*f2
        f3 = func([x_0+step, y_0+k3])
        k4 = step*f3
        y_0 += (1/6)*(k1+2*k2+2*k3+k4)
        x_0 += step
        puntos_x.append(x_0)
        puntos_y.append(y_0)
    return [puntos_x, puntos_y]

def func(lista):
    return 2*lista[0]-6    

main()


