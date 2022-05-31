import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd #Permite la apertura de ventanas emergentes para guardar y seleccionar archivos
from tkinter.messagebox import showinfo
import matplotlib.pyplot as plt 


import pandas as pd


#-------------------------- Ventana de trabajo principal ------------------------

#Creo la ventana principal
root= tk.Tk()
root.title('Aplicación para el cálculo de la radiación diaria')
root.resizable(False, False)
root.geometry('450x200')

root.columnconfigure(0, weight=1) #Define que sólo voy a tener una columna y que se va a expandir si se redimensiona la app

#Encabezado de la aplicación
ttk.Label(
    root, text="Cálculo de radiación diaria mensual en Wh/m2",
    font=("TkDefaultFont", 16)
    ).grid()

#------------------------ Definición de variables globales ----------------------

mes_var= tk.StringVar(value='') #Variable donde guardar el mes en el que voy a calcular la radiación

#ruta_archivo= tk.StringVar(value='')
ruta_archivo= list()

#--------------------------- Definición de funciones ---------------------------

def on_select_file():
    global ruta_archivo

    filetypes = (
        ('text files', '*.csv'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Abrir archivo',
        initialdir='/',
        filetypes=filetypes)

    showinfo(
        title='Fila seleccionada',
        message=filename
    )
    ruta_archivo.append(filename)
    print(ruta_archivo)


def on_reset_file():
    global ruta_archivo
    ruta_archivo = []
    print(ruta_archivo)

def on_ver_archivos():
    cant_archivos= len(ruta_archivo)
    mensaje= f'Cantidad de archivos: {cant_archivos} \n'
    for string in ruta_archivo:
        mensaje += string + '\n'

    showinfo(
        title= 'Filas seleccionadas',
        #Debo agregar un bucle for para crear message
        message= mensaje
    )

def on_calcular_rad():
    """Calcula el valor de la radiación diaria mensual y grafica algunos días"""
    global ruta_archivo
    global mes_var
    
    df_list= [] #Creo una lista que puede contener más de un dataframe

    for ruta in ruta_archivo:
        df_list.append(pd.read_csv(ruta, usecols=[0,2], names=['fechaHora', 'CR1000'],
                    skiprows=4, index_col=0, parse_dates=True))

    df= pd.concat(df_list, axis=0)
    print(df.head())

    plt.plot(df.index, df.CR1000)

#-------------------------- Marco de trabajo principal ------------------------

frame_principal= ttk.LabelFrame(root)
frame_principal.grid(padx=10, sticky=(tk.E + tk.W))
frame_principal.columnconfigure(0, weight=1)


#-------------------------- Marco de selección de archivos ------------------------

sel_archivos = ttk.LabelFrame(frame_principal, text='Selección de archivos')
sel_archivos.grid(sticky=(tk.W + tk.E))

for i in range(3):
    sel_archivos.columnconfigure(i, weight=1)

ttk.Button(sel_archivos, text='Agregar archivos', command= on_select_file).grid(row=0, column=0)

ttk.Button(sel_archivos, text='Reset', command= on_reset_file).grid(row=0, column=1)

ttk.Button(sel_archivos, text='Ver archivos', command= on_ver_archivos).grid(row=0, column=2)


#-------------------------- Marco para cálculos de radiación ------------------------

frame_rad= ttk.LabelFrame(frame_principal, text='Cálculos de radiación')
frame_rad.grid(sticky=(tk.W + tk.E))

for i in range(3):
    frame_rad.columnconfigure(i, weight=1)

meses= ['enero', 'febrero', 'marzo']
ttk.Combobox(frame_rad, values= meses, textvariable= mes_var).grid(row=0, column=0)
ttk.Label(frame_rad, text='Seleccionar mes').grid(row=1, column=0)

ttk.Button(frame_rad, text= 'Calcular radiación diaria', command= on_calcular_rad).grid(row=0, column=1)

ttk.Button(frame_rad, text= 'Ver gráfico para').grid(row=0, column=2)


#Correr programa
root.mainloop()


















