from tkinter import *
from tkinter import ttk
import sqlite3 #modulo de conexion a DB


#metodos CRUD
class Product:

    #constructor de la Clase
    def __init__(self, frm_Form):
        self.frm = frm_Form

        self.frm.title('Market App')

        #creacion de un Frame Contenedor
        frame = LabelFrame(self.frm, text='Register a new Product') #creacion
        frame.grid(row=0, column=0, columnspan=3, pady=20) #posicionamiento
        
        #Name Input  
        Label(frame, text='Name: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus() #focus en name
        self.name.grid(row = 1, column = 1)

        #Price input
        Label(frame, text='Price: ').grid(row = 2, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)

        #Button add product
        ttk.Button(frame, text = 'Save Product').grid(row = 3, columnspan = 2, sticky =  W + E)






#arraque de app
if __name__ == '__main__':
    frm_Form = Tk()
    app = Product(frm_Form)
    frm_Form.mainloop()