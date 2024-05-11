from tkinter import *
from tkinter import ttk
from tkinter import messagebox 
#Python image Library
from PIL import ImageTk, Image
from subprocess import call
import sqlite3
import subprocess

class DatabaseOperations:
    db_name='database_proyecto.db'

    def Ejecutar_consulta(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conexion:
            cursor=conexion.cursor()
            result=cursor.execute(query,parameters)
            conexion.commit()
        return result 
    
    def Buscar_usuario(self, dni, respuesta):
        with sqlite3.connect(self.db_name) as conexion:
            cursor=conexion.cursor()
            sql=f"SELECT * FROM Usuarios WHERE DNI = {dni} AND Respuesta = '{respuesta}'"
            cursor.execute(sql)
            busqueda= cursor.fetchall() # obtener respuesta como lista
            cursor.close()
            return busqueda
        
class validador:

    def __init__(self, siguiente=None):
        self._siguiente = siguiente

    def set_siguiente(self, siguiente):
        self._siguiente = siguiente
        return self._siguiente
    
    def validar(self, *args, **kwargs):
        if self._siguiente:
            return self._siguiente.validar(*args, **kwargs)

    @staticmethod
    def Validar_formulario_completo(dni,nuevo_password,repetir_password,respuesta):
        if len(dni) !=0 and len(nuevo_password) !=0 and len(repetir_password) !=0 and len(respuesta) !=0:
            return True
        else:
             messagebox.showerror("ERROR", "Complete todos los campos del formulario")

    @staticmethod       
    def Validar_contraseña(nuevo_password,repetir_password):
        if(str(nuevo_password) == str(repetir_password)):
            return True
        else:
            messagebox.showerror("ERROR DE RECUPERACION", "Contraseñas no coinciden")

    @staticmethod
    def Validar_datos_usuario(dni,respuesta,db):
        busqueda = db.Buscar_usuario(dni, respuesta)
        if (busqueda != []):
            return True
        else:
            messagebox.showerror("ERROR DE RECUPERACION", "Datos de recuperacion no son correctos")

class Recuperar_contraseña:
   
    ruta_script_login = r"C:\Users\Jhon\Desktop\practica_especializaciom\proyecto_final\Login2.py"
    
    def __init__(self, ventana_recuperar):
        self.window=ventana_recuperar   
        self.window.title("RECUPERAR CONTASEÑA")
        self.window.geometry("410x420")
        self.window.resizable(0,0)
        self.window.config(bd=10)
        self.create_widgets()
        self.validator=validador()
        self.db=DatabaseOperations()

    def create_widgets(self):
        "--------------- Titulo --------------------"
        titulo= Label(ventana_recuperar, text="RECUPERAR CONTRASEÑA",fg="black",font=("Comic Sans", 13,"bold"),pady=8).pack()

  
        "--------------- Marco --------------------"
        marco = LabelFrame(ventana_recuperar, text="Datos de recuperacion",font=("Comic Sans", 10,"bold"))
        marco.config(bd=2)
        marco.pack()

        "--------------- Formulario --------------------"
        label_dni=Label(marco,text="DNI: ",font=("Comic Sans", 10,"bold")).grid(row=0,column=0,sticky='s',padx=5,pady=8)
        self.dni=Entry(marco,width=25)
        self.dni.focus()
        self.dni.grid(row=0, column=1, padx=5, pady=8)
        
        label_nota=Label(marco,text="*Seleccione una pregunta y brinde la respuesta correcta.",font=("Comic Sans", 9,"bold"),foreground="blue").grid(row=1,column=0,columnspan=2,sticky='s',padx=8)

        label_pregunta=Label(marco,text="Pregunta: ",font=("Comic Sans", 10,"bold")).grid(row=2,column=0,sticky='s',padx=5,pady=8)
        self.combo_pregunta=ttk.Combobox(marco,values=["¿Nombre de tu primera mascota?","¿Lugar dónde fuiste al colegio?","¿En que ciudad naciste?","¿Cómo se llama tu equipo favorito?"], width=30,state="readonly")
        self.combo_pregunta.current(0)
        self.combo_pregunta.grid(row=2,column=1,padx=5,pady=8)

        label_respuesta=Label(marco,text="Respuesta: ",font=("Comic Sans", 10,"bold")).grid(row=3,column=0,sticky='s',padx=5,pady=8)
        self.respuesta=Entry(marco,width=33)
        self.respuesta.grid(row=3, column=1, padx=5, pady=8)

        label_password=Label(marco,text="Nueva Contraseña: ",font=("Comic Sans", 10,"bold")).grid(row=4,column=0,sticky='s',padx=5,pady=8)
        self.nuevo_password=Entry(marco,width=25,show="*")
        self.nuevo_password.grid(row=4, column=1, padx=5, pady=8)

        label_password=Label(marco,text="Repetir contraseña: ",font=("Comic Sans", 10,"bold")).grid(row=5,column=0,sticky='s',padx=10,pady=8)
        self.repetir_password=Entry(marco,width=25,show="*")
        self.repetir_password.grid(row=5, column=1, padx=5, pady=8)

        "--------------- Frame botones --------------------"
        frame_botones=Frame(ventana_recuperar)
        frame_botones.pack()

        "--------------- Botones --------------------"
        boton_recuperar=Button(frame_botones,text="RECUPERAR",command=self.Restablecer_contraseña ,height=2,width=10,bg="green",fg="white",font=("Comic Sans", 10,"bold")).grid(row=0, column=1, padx=10, pady=10)
        boton_cancelar=Button(frame_botones,text="CANCELAR",command=self.LLamar_login ,height=2,width=10,bg="red",fg="white",font=("Comic Sans", 10,"bold")).grid(row=0, column=3, padx=10, pady=10)
        
    
    
    def Restablecer_contraseña(self):
        if self.validator.Validar_formulario_completo(self.dni.get(),self.nuevo_password.get(),self.repetir_password.get(),self.respuesta.get()) and self.validator.Validar_datos_usuario(self.dni.get(),self.respuesta.get(),self.db) and self.validator.Validar_contraseña(self.nuevo_password.get(),self.repetir_password.get()):
            query='UPDATE Usuarios SET CONTRASEÑA = (?) WHERE DNI= (?)'
            parameters = (self.nuevo_password.get(), self.dni.get())
            self.db.Ejecutar_consulta(query, parameters)
            messagebox.showinfo("CONTRASEÑA RECUPERADA", f'Contraseña actualizada correctamente: {self.nuevo_password.get()}')
            print('DATOS ACTUALIZADO')
            self.Limpiar_formulario()
    
    def Limpiar_formulario(self):
        self.dni.delete(0, END)
        self.respuesta.delete(0, END)
        self.nuevo_password.delete(0, END)
        self.repetir_password.delete(0, END)     
        
    def LLamar_login(self):
        ventana_recuperar.destroy()    
        subprocess.call(['python',self.ruta_script_login])

            
if __name__ == '__main__':
    ventana_recuperar=Tk()
    application=Recuperar_contraseña(ventana_recuperar)
    ventana_recuperar.mainloop()