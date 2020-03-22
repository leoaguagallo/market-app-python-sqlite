from tkinter import *
import sqlite3 #modulo de conexion a DB


#metodos CRUD
class Product:

    #constructor de la Clase
    def __init__(self, frm_Form):
        self.frm = frm_Form
        self.frm.title('Market App')


#arraque de app
if __name__ == '__main__':
    frm_Form = Tk()
    app = Product(frm_Form)
    frm_Form.mainloop()