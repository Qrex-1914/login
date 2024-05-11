from tkinter import *
from tkinter import ttk
from tkinter import messagebox 
#Python image Library
from PIL import ImageTk, Image
from subprocess import call
import sqlite3
import subprocess
from abc import ABC,abstractmethod

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
        
class Validador:
    def __init__(self, siguiente=None):
        self._siguiente = siguiente

    def set_siguiente(self, siguiente):
        self._siguiente = siguiente

    def validar(self, data):
        pass
    

class ValidarFormularioCompleto(Validador):
    def validar(self, data):
        if len(data['dni']) !=0 and len(data['nuevo_password']) !=0 and len(data['repetir_password']) !=0 and len(data['respuesta']) !=0:
            if self._siguiente:
                return self._siguiente.validar(data)
            return True
        else:
            return False

class ValidarContraseña(Validador):
    def validar(self, data):
        if data['nuevo_password'] == data['repetir_password']:
            if self._siguiente:
                return self._siguiente.validar(data)
            return True
        else:
            return False

        
class ValidarDatosUsuario(Validador):

    def __init__(self, db, siguiente=None):
        super().__init__(siguiente)
        self.db = db
        
    def validar(self, data):
        self.db=DatabaseOperations()
        busqueda = self.db.Buscar_usuario(data['dni'], data['respuesta'])
        if busqueda != []:
            if self._siguiente:
                return self._siguiente.validar(data)
            return True
        else:
            return False
    

class Recuperar_contraseña:
   
    ruta_script_login = r"C:\Users\Jhon\Desktop\practica_especializaciom\proyecto_final\Login2.py"
    
    def __init__(self, ventana_recuperar):
        self.window=ventana_recuperar   
        self.window.title("RECUPERAR CONTASEÑA")
        self.window.geometry("410x420")
        self.window.resizable(0,0)
        self.window.config(bd=10)
        self.create_widgets()
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
        validador1 = ValidarFormularioCompleto()
        validador2 = ValidarContraseña()
        validador3 = ValidarDatosUsuario(self.db)

        validador1.set_siguiente(validador2)
        validador2.set_siguiente(validador3)

        data = {
            'dni': self.dni.get(),
            'nuevo_password': self.nuevo_password.get(),
            'repetir_password': self.repetir_password.get(),
            'respuesta': self.respuesta.get()
        }

        if validador1.validar(data):
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