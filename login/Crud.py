"""
CRUD-Passwords
-Registro de Prouctos
-Guardar en bd SQlite

"""
from tkinter import *
from tkinter import ttk
from tkinter import messagebox 
import sqlite3
import random
import os

class Pass:
    db_name='database_proyecto.db'
    dni=os.environ['dni']
    def __init__(self, ventana_pass):

        self.window=ventana_pass   
        self.window.title("APLICACION")
        self.window.geometry("800x670")
        self.window.resizable(0,0)
        self.window.config(bd=10)
        
        
        
        "--------------- Titulo --------------------"
        titulo= Label(ventana_pass, text="REGISTRO DE CONTRASEÑAS",fg="black",font=("Comic Sans", 17,"bold"),pady=10).pack()

        "--------------- label funcion random --------------------"
        frame_logo_productos = LabelFrame(ventana_pass)
        frame_logo_productos.config(bd=0)
        frame_logo_productos.pack()


        "--------------- Frame marco --------------------"
        marco = LabelFrame(ventana_pass, text="Informacion de la contraseña",font=("Comic Sans", 10,"bold"),pady=5)
        marco.config(bd=2)
        marco.pack()

        "--------------- Formulario --------------------"
        label_pagina=Label(marco,text="Pagina: ",font=("Comic Sans", 10,"bold")).grid(row=0,column=0,sticky='s',padx=5,pady=8)
        self.pagina=Entry(marco,width=25)
        self.pagina.focus()
        self.pagina.grid(row=0, column=1, padx=5, pady=8)
        
        label_contraseña=Label(marco,text="Contraseña: ",font=("Comic Sans", 10,"bold")).grid(row=1,column=0,sticky='s',padx=5,pady=8)
        self.contraseña=Entry(marco,width=25)
        self.contraseña.grid(row=1, column=1, padx=5, pady=8)
        
        "--------------- Frame botones --------------------"
        frame_botones=Frame(ventana_pass)
        frame_botones.pack()

        "--------------- Botones --------------------"
        boton_registrar=Button(frame_botones,text="REGISTRAR",command=self.Agregar_contraseña,height=2,width=10,bg="green",fg="white",font=("Comic Sans", 10,"bold")).grid(row=0, column=1, padx=10, pady=15)
        boton_editar=Button(frame_botones,text="EDITAR",command=self.Editar_contraseña ,height=2,width=10,bg="gray",fg="white",font=("Comic Sans", 10,"bold")).grid(row=0, column=2, padx=10, pady=15)
        boton_eliminar=Button(frame_botones,text="ELIMINAR",command=self.Eliminar_contraseña,height=2,width=10,bg="red",fg="white",font=("Comic Sans", 10,"bold")).grid(row=0, column=3, padx=10, pady=15)
        boton_generar_contraseña=Button(frame_botones,text="CONTRASEÑA",command=self.generar_contraseña,height=2,width=10,bg="blue",fg="white",font=("Comic Sans", 10,"bold")).grid(row=0, column=4, padx=10, pady=15)
        "--------------- Tabla --------------------"    
        self.tree=ttk.Treeview(height=13, columns=("columna1","columna2",))
        self.tree.heading("#0",text='ID', anchor=CENTER)
        self.tree.column("#0", width=90, minwidth=75, stretch=NO)
        
        self.tree.heading("columna1",text='PAGINA', anchor=CENTER)
        self.tree.column("columna1", width=150, minwidth=75, stretch=NO)
        
        
        self.tree.heading("columna2",text='CONTRASEÑA', anchor=CENTER)
        self.tree.column("columna2", width=150, minwidth=75, stretch=NO)
        
        self.tree.pack()
        
        self.Obtener_contraseña()

    "--------------- CRUD --------------------"               
    def Obtener_contraseña(self):
        records=self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query=f'SELECT * FROM TABLA_{self.dni} ORDER BY ID desc'
        db_rows=self.Ejecutar_consulta(query)
        for row in db_rows:
            self.tree.insert("", 0,text=row[0],values=(row[1],row[2]))

        #text=row[0],
            
    def Agregar_contraseña(self):
        if self.Validar_formulario_completo():
            query=f'INSERT INTO TABLA_{self.dni} VALUES(NULL, ?, ?)'
            parameters = (self.pagina.get(),self.contraseña.get())
            self.Ejecutar_consulta(query, parameters)
            messagebox.showinfo("REGISTRO EXITOSO", f'pagina registrada: {self.pagina.get()}')
            print('REGISTRADO')
        self.Limpiar_formulario()
        self.Obtener_contraseña()
    
    def Eliminar_contraseña(self):
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            messagebox.showerror("ERROR","Porfavor selecciona un elemento") 
            return
        dato=self.tree.item(self.tree.selection())['text']
        pagina=self.tree.item(self.tree.selection())['values'][0]
        query=f"DELETE FROM TABLA_{self.dni} WHERE PAGINA = ?"
        respuesta=messagebox.askquestion("ADVERTENCIA",f"¿Seguro que desea eliminar la pagihna: {pagina}?")
        if respuesta == 'yes':
            self.Ejecutar_consulta(query,(pagina,))
            self.Obtener_contraseña()
            messagebox.showinfo('EXITO',f'Producto eliminado: {pagina}')
        else:
            messagebox.showerror('ERROR',f'Error al eliminar el producto: {pagina}')
     
    def Editar_contraseña(self):
        try:
            self.tree.item(self.tree.selection())['text']
        except IndexError as e:
            messagebox.showerror("ERROR","Porfavor selecciona un elemento") 
            return
        pagina=self.tree.item(self.tree.selection())['values'][0]
        contraseña=self.tree.item(self.tree.selection())['values'][1]
       
        self.Ventana_editar = Toplevel()
        self.Ventana_editar.title('EDITAR CONTRASEÑA')
        self.Ventana_editar.resizable(0,0)
        
        
        #Valores ventana editar
        label_pagina=Label(self.Ventana_editar,text="Pagina: ",font=("Comic Sans", 10,"bold")).grid(row=0,column=0,sticky='s',padx=5,pady=8)
        nuevo_pagina=Entry(self.Ventana_editar,textvariable=StringVar(self.Ventana_editar,value=pagina),width=25)
        nuevo_pagina.grid(row=0, column=1, padx=5, pady=8)
        
        label_contraseña=Label(self.Ventana_editar,text="Contraseña: ",font=("Comic Sans", 10,"bold")).grid(row=1,column=0,sticky='s',padx=5,pady=8)
        nuevo_contraseña=Entry(self.Ventana_editar,textvariable=StringVar(self.Ventana_editar,value=contraseña),width=25)
        nuevo_contraseña.grid(row=1, column=1, padx=5, pady=8)

        boton_actualizar=Button(self.Ventana_editar,text="ACTUALIZAR",command= lambda: self.Actualizar(nuevo_pagina.get(),nuevo_contraseña.get(),pagina,contraseña),height=2,width=20,bg="black",fg="white",font=("Comic Sans", 10,"bold"))
        boton_actualizar.grid(row=3, column=1,columnspan=2, padx=10, pady=15)
        
        self.Ventana_editar.mainloop()      
    

    def Actualizar(self,nuevo_pagina,nuevo_contraseña,pagina,contraseña):
        query=f'UPDATE TABLA_{self.dni} SET PAGINA = ?, CONTRASEÑA = ? WHERE PAGINA = ? AND CONTRASEÑA =?'
        parameters=(nuevo_pagina,nuevo_contraseña,pagina,contraseña)
        self.Ejecutar_consulta(query,parameters)
        messagebox.showinfo('EXITO',f'Producto actualizado:{nuevo_pagina}')
        self.Ventana_editar.destroy()
        self.Obtener_contraseña() 

    #generador de contraseñas
    def contraseñas_aleatorias(self):
        letras="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        numeros="0123456789"
        simbolos="#@=<>{[]}?¿-;}][]}"
        
        unir = f'{letras}{numeros}{simbolos}'
        longitud=12
        contraseña=random.sample(unir,longitud)
        password_final = "".join(contraseña)
        return password_final
    #funcion para generar contraseña
    def generar_contraseña(self):
        self.Ventana_contraseña = Toplevel()
        self.Ventana_contraseña.title('EDITAR CONTRASEÑA')
        #self.Ventana_contraseña.resizable(0,0)
        print("boton oprimido")

        contraseña=self.contraseñas_aleatorias()
        #ventana nueva para ver contraseña 
        #Valores ventana editar
        label_contras_aleatorias=Label(self.Ventana_contraseña,text="Contraseña: ",font=("Comic Sans", 10,"bold")).grid(row=0,column=0,sticky='s',padx=5,pady=8)
       
        nueva_contraseña = Entry(self.Ventana_contraseña, width=25)
        nueva_contraseña.insert(0, contraseña)
        nueva_contraseña.grid(row=0, column=1, padx=5, pady=8)

        self.Ventana_contraseña.mainloop()      
    
    "--------------- OTRAS FUNCIONES --------------------"
    def Ejecutar_consulta(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conexion:
            cursor=conexion.cursor()
            result=cursor.execute(query,parameters)
            conexion.commit()
        return result   
          
    def Validar_formulario_completo(self):
        if len(self.pagina.get()) !=0 and len(self.contraseña.get()) !=0 :
            return True
        else:
             messagebox.showerror("ERROR", "Complete todos los campos del formulario") 
    
    def Limpiar_formulario(self):
        self.pagina.delete(0, END)
        self.contraseña.delete(0, END)
       
               
if __name__ == '__main__':
    ventana_pass=Tk()
    application=Pass(ventana_pass)
    ventana_pass.mainloop()