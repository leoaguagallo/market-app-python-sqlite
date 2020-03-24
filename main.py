from tkinter import *
from tkinter import ttk
import sqlite3 #modulo de conexion a DB


#metodos CRUD
class Product:

    db_name = 'database.db' #bd

    #------GUI-------------
    #constructor de la Clase
    def __init__(self, frm_Form):
        self.frm = frm_Form

        self.frm.title('Market App')

        #creacion de un Frame Contenedor
        frame = LabelFrame(self.frm, text='Register a new Product') #creacion
        frame.grid(row=0, column=0, columnspan=3, pady=20) #posicionamiento
        
        #Name Input  
        Label(frame, text='Name: ').grid(row = 1, column = 0) #creacion
        self.name = Entry(frame) #add to frame
        self.name.focus() #focus en name
        self.name.grid(row = 1, column = 1) #posicion

        #Price input
        Label(frame, text='Price: ').grid(row = 2, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)

        #Button add product
        ttk.Button(frame, text = 'Save Product', command = self.add_products).grid(row = 3, columnspan = 2, sticky =  W + E)

        #Output Messagess
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 3 , column = 0, columnspan = 2, sticky = W + E)

        #table on frame
        self.table_model = ttk.Treeview(height = 10, columns = 2) #creacion
        self.table_model.grid(row = 4, column = 0, columnspan = 2) #posicion
        self.table_model.heading('#0', text='Name', anchor=CENTER) #titulo
        self.table_model.heading('#1', text='Price', anchor=CENTER)

        #Delete and update buttons
        ttk.Button(text = 'DELETE', command = self.delete_products).grid(row = 5, column = 0, sticky = W + E)
        ttk.Button(text = 'EDIT', command=self.edit_products).grid(row = 5, column = 1, sticky = W + E)

        #print products
        self.get_products()

    #-------Data Base--------
    #Connection and query the database
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    #Get product
    def get_products(self):
        self.cleaning_table()
        #quering data    
        query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)
        self.filling_data(db_rows) #filling data on table
    
    #Add products
    def add_products(self):
        if self.field_validation():
            query = 'INSERT INTO product VALUES(NULL, ?, ?)'
            parameters = (self.name.get(), self.price.get())
            self.run_query(query, parameters)
            
            self.message['text'] = 'Product {} added Successfully'.format(self.name.get()) #update messagess
            self.name.delete(0, END) #cleaning inputs
            self.price.delete(0, END)

        else:
            self.message['text'] = 'Name and price is required!!'
            self.name.focus() #focus en name
        
        self.get_products()

    #Delete products
    def delete_products(self):
        self.message['text'] = ''
        try:
            self.table_model.item(self.table_model.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please Select a record'
            return
        
        self.message['text'] = ''
        name = self.table_model.item(self.table_model.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query, (name,))
        
        self.message['text'] = 'Record {} deleted Successfully'.format(name)
        self.get_products()

    #Edit products
    def edit_products(self):
        self.message['text'] = ''
        try:
            self.table_model.item(self.table_model.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please Select a record'
            return

        name = self.table_model.item(self.table_model.selection())['text']
        old_price = self.table_model.item(self.table_model.selection())['values'][0]

        #Auxiliar edit Form-----------------------
        self.auxiliar_form(name, old_price)

    #Update Recors
    def edit_records(self, new_name, name, new_price, old_price):
        query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (new_name, new_price, name, old_price)
        self.run_query(query, parameters)

        self.edit_frm.destroy()
        self.message['text'] = 'Record {} updated Successfully'.format(name)
        self.get_products()


    #creating edit form
    def auxiliar_form(self, name, old_price):
        
        self.edit_frm = Toplevel()
        self.edit_frm.title = 'Edit Products'

        #input old name
        Label(self.edit_frm, text='Old Name: ').grid(row = 0, column = 1) #etiqueta
        Entry(self.edit_frm, textvariable = StringVar(self.edit_frm, value = name), state = 'readonly').grid(row = 0, column = 2) #input area

        #input new name
        Label(self.edit_frm, text='New Name: ').grid(row = 1, column = 1) #etiqueta
        new_name = Entry(self.edit_frm)
        new_name.grid(row = 1, column = 2)

        #Input old price
        Label(self.edit_frm, text='Old Price: ').grid(row = 2, column = 1) #etiqueta
        Entry(self.edit_frm, textvariable = StringVar(self.edit_frm, value = old_price), state = 'readonly').grid(row = 2, column = 2) #input area

        #Input new price
        Label(self.edit_frm, text='New price: ').grid(row = 3, column = 1) #etiqueta
        new_price = Entry(self.edit_frm)
        new_price.grid(row = 3, column = 2)

        #Button
        Button(self.edit_frm, text = 'Update', command = lambda: self.edit_records(new_name.get(), name, new_price.get(), old_price)).grid(row = 4, column = 2, sticky = W)
        self.edit_frm.mainloop()


        
    #-------Tools---------------
    #cleaning table
    def cleaning_table(self):
        records = self.table_model.get_children()
        for elem in records:
            self.table_model.delete(elem)
    
    #filling data on table
    def filling_data(self, db_rows):
        for row in db_rows:
            self.table_model.insert('', 0, text = row[1], values = row[2])

    #field validation
    def field_validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    

#arraque de app
if __name__ == '__main__':
    frm_Form = Tk()
    app = Product(frm_Form)
    frm_Form.mainloop()