"""
FORMULARIO DE LOGIN
Ingresar al sistema con su dni y contraseña
Mostrar messagebox
"""
from tkinter import *
from tkinter import ttk
from tkinter import messagebox 
import sqlite3
import subprocess
import os


class DatabaseManager:
    db_name='database_proyecto.db'
    tabla='Usuarios'
    def __init__(self):
        pass

    #crea la base de datos
    def createDB(self):
        conn = sqlite3.connect(self.db_name)
        conn.commit()
        conn.close()

     #crear la tabla el usuario
    def createTable(self):
        # Verificar si la tabla ya existe
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (self.tabla,))
            table_exists = cursor.fetchone()
            
            if not table_exists:
                # La tabla no existe, entonces la creamos
                cursor.execute(
                    f"""CREATE TABLE {self.tabla} (
                        ID integer PRIMARY KEY AUTOINCREMENT,
                        DNI integer UNIQUE,
                        NOMBRE varchar,
                        EMAIL varchar,
                        CONTRASEÑA varchar,
                        RESPUESTA varchar
                    )"""
                )   

    def Validar_login(self, dni, password):
        self.dni=dni
        self.password=password
        with sqlite3.connect(self.db_name) as conexion:
            cursor=conexion.cursor()
            sql= f"SELECT * FROM Usuarios WHERE DNI = {self.dni} AND CONTRASEÑA = '{self.password}'"
            cursor.execute(sql)
            validacion= cursor.fetchall() # obtener respuesta como lista
            cursor.close()
            return validacion


class Login():
    ruta_script_registro = r"C:\Users\Jhon\Desktop\practica_especializaciom\proyecto_final\login\Formulario_de_registro.py"
    ruta_script_recuperar=r"C:\Users\Jhon\Desktop\practica_especializaciom\proyecto_final\login\Recuperar_contraseña.py"
    ruta_script_ingresar=r"C:\Users\Jhon\Desktop\practica_especializaciom\proyecto_final\login\Crud.py"
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
        
        "--------------- Frame botones --------------------"
        frame_botones=Frame(ventana_login)
        frame_botones.pack()

        "--------------- Botones --------------------"
        boton_ingresar=Button(frame_botones,text="INGRESAR",command=self.Login,height=2,width=12,bg="green",fg="white",font=("Comic Sans", 10,"bold")).grid(row=0, column=1, padx=10, pady=15)
        boton_registrar=Button(frame_botones,text="REGISTRAR",command=self.LLamar_registro,height=2,width=12,bg="blue",fg="white",font=("Comic Sans", 10,"bold")).grid(row=0, column=2, padx=10, pady=15)
        label_=Label(frame_botones,text="⬇ ¿Olvido su contraseña? ⬇",font=("Comic Sans", 10,"bold")).grid(row=1,column=1,columnspan=2,sticky='s')
        boton_olvido=Button(frame_botones,text="RECUPERAR CONTRASEÑA",command=self.LLamar_recuperar ,height=2,width=24,bg="gray",fg="white",font=("Comic Sans", 10,"bold")).grid(row=2, column=1, columnspan=2, padx=10, pady=8)
    
        
    def Validar_formulario_completo(self):
        if len(self.dni.get()) !=0 and len(self.password.get()) !=0:
            return True
        else:
             messagebox.showerror("ERROR DE INGRESO", "Ingrese su DNI y contraseña!!!")    
    
    def Login(self):
        if(self.Validar_formulario_completo()):
            dni= self.dni.get()
            password= self.password.get()
            dato = self.db_manager.Validar_login(dni, password)
            if (dato != []):
                self.LLamar_crud()
                #messagebox.showinfo("BIENVENIDO", "Datos ingresados correctamente")

            else:
                messagebox.showerror("ERROR DE INGRESO", "DNI o contraseña incorrecto") 
                  

    #call recuperar        
    def LLamar_recuperar(self):
        ventana_login.destroy()    
        subprocess.call(['python',self.ruta_script_recuperar])
    
    #call registro              
    def LLamar_registro(self):
        ventana_login.destroy()    
        subprocess.call(['python',self.ruta_script_registro])

    #call crud           
    def LLamar_crud(self):
        os.environ['dni']=self.dni.get()
        ventana_login.destroy()    
        subprocess.call(['python',self.ruta_script_ingresar])

    

#verificar si el modulo ha sido ejecutado correctamente  
if __name__ == '__main__':
    ventana_login=Tk()
    db_manager=DatabaseManager()
    application=Login(ventana_login,db_manager)
    ventana_login.mainloop()