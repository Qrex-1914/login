"""
FORMULARIO DE LOGIN
Ingresar al sistema con su dni y contraseña
Mostrar messagebox
"""
from tkinter import *
from tkinter import ttk
from tkinter import messagebox 
import subprocess
import os
from db import DatabaseManager
from newLogin import Login

class create_login_interface():
    ruta_script_registro = r"C:\Users\Jhon\Desktop\practica_especializaciom\proyecto_final\Formulario_de_registro.py"
    ruta_script_recuperar=r"C:\Users\Jhon\Desktop\practica_especializaciom\proyecto_final\Recuperar_contraseña.py"
    ruta_script_ingresar=r"C:\Users\Jhon\Desktop\practica_especializaciom\proyecto_final\Crud.py"
    #ruta_script = os.path.normpath(ruta_script)

    def __init__(self,ventana_login,db_manager):
        self.window=ventana_login  
        self.window.title("INGRESAR AL SISTEMA")
        self.window.geometry("330x370")
        self.window.resizable(0,0)
        self.window.config(bd=10)
        
        # Crear la base de datos y la tabla al inicio
        self.db_manager=db_manager
        self.db_manager.createDB()
        self.db_manager.createTable()
        
        "--------------- Titulo --------------------"
        titulo= Label(ventana_login, text="INICIAR SESION",fg="black",font=("Comic Sans", 13,"bold"),pady=10).pack()

        "--------------- Marco --------------------"
        marco = LabelFrame(ventana_login, text="Ingrese sus datos",font=("Comic Sans", 10,"bold"))
        marco.config(bd=2)
        marco.pack()

        "--------------- Formulario --------------------"
        label_dni=Label(marco,text="DNI: ",font=("Comic Sans", 10,"bold")).grid(row=0,column=0,sticky='s',padx=5,pady=10)
        self.dni=Entry(marco,width=25)
        self.dni.focus()
        self.dni.grid(row=0, column=1, padx=5, pady=10)

        label_nombres=Label(marco,text="Contraseña: ",font=("Comic Sans", 10,"bold")).grid(row=1,column=0,sticky='s',padx=10,pady=10)
        self.password=Entry(marco,width=25,show="*")
        self.password.grid(row=1, column=1, padx=10, pady=10)
        
        
        self.login=Login(self.dni.get(),self.password.get(),self.db_manager)
        "--------------- Frame botones --------------------"
        frame_botones=Frame(ventana_login)
        frame_botones.pack()

        "--------------- Botones --------------------"
        boton_ingresar=Button(frame_botones,text="INGRESAR",command=self.login.get_access,height=2,width=12,bg="green",fg="white",font=("Comic Sans", 10,"bold")).grid(row=0, column=1, padx=10, pady=15)
        boton_registrar=Button(frame_botones,text="REGISTRAR",command=self.LLamar_registro,height=2,width=12,bg="blue",fg="white",font=("Comic Sans", 10,"bold")).grid(row=0, column=2, padx=10, pady=15)
        label_=Label(frame_botones,text="⬇ ¿Olvido su contraseña? ⬇",font=("Comic Sans", 10,"bold")).grid(row=1,column=1,columnspan=2,sticky='s')
        boton_olvido=Button(frame_botones,text="RECUPERAR CONTRASEÑA",command=self.LLamar_recuperar ,height=2,width=24,bg="gray",fg="white",font=("Comic Sans", 10,"bold")).grid(row=2, column=1, columnspan=2, padx=10, pady=8)
    
        
    #call recuperar        
    def LLamar_recuperar(self):
        self.window.destroy()    
        subprocess.call(['python',self.ruta_script_recuperar])
    
    #call registro              
    def LLamar_registro(self):
        self.window.destroy()    
        subprocess.call(['python',self.ruta_script_registro])



    

