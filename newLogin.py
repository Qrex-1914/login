
from tkinter import *
from tkinter import messagebox 
import os
import subprocess
class Login:
    def __init__(self,dni,password,db_manager):
        self.dni=dni
        self.password=password
        self.db_manager=db_manager
        print(self.dni,self.password)
    def get_access(self):
        if(self.Validar_formulario_completo):
            dato = self.db_manager.Validar_login(self.dni, self.password)
            print(dato)
            if (dato != []):
                self.connect_crud()
            else:
                messagebox.showerror("ERROR DE INGRESO", "DNI o contraseña incorrecto") 

    def Validar_formulario_completo(self):
        if len(self.dni) !=0 and len(self.password) !=0:
            return True
        else:
                messagebox.showerror("ERROR DE INGRESO", "Ingrese su DNI y contraseña!!!")          
    def connect_crud(self):
        os.environ['dni']=self.dni.get()
        self.window.destroy()    
        subprocess.call(['python',self.ruta_script_ingresar])