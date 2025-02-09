
#FORMULARIO DE REGISTRO DE USUARIO
#-Registro de usuario y contraseña
#-Guardar en bd SQlite

from tkinter import *
from tkinter import ttk
from tkinter import messagebox 
import sqlite3
import subprocess





class Registro:
    db_name='database_proyecto.db'
    ruta_script_login=r"C:\Users\Jhon\Desktop\practica_especializaciom\proyecto_final\login\Login.py"
    
    def __init__(self,vetana):
        self.window=ventana   
        self.window.title("FORMULARIO DE REGISTRO")
        self.window.geometry("390x450")
        self.window.resizable(0,0)
        self.window.config(bd=10)
        self.create_widgets()
    
    def create_widgets(self):
        "--------------- Titulo --------------------"
        titulo= Label(ventana, text="REGISTRO DE USUARIO",fg="black",font=("Comic Sans", 13,"bold"),pady=5).pack()

        "--------------- Marco --------------------"
        marco = LabelFrame(ventana, text="Datos personales",font=("Comic Sans", 10,"bold"))
        marco.config(bd=2,pady=5)
        marco.pack()

        "--------------- Formulario --------------------"
        label_dni=Label(marco,text="DNI: ",font=("Comic Sans", 10,"bold")).grid(row=0,column=0,sticky='s',padx=5,pady=8)
        self.dni=Entry(marco,width=25)
        self.dni.focus()
        self.dni.grid(row=0, column=1, padx=5, pady=8)

        label_nombres=Label(marco,text="Nombre: ",font=("Comic Sans", 10,"bold")).grid(row=1,column=0,sticky='s',padx=10,pady=8)
        self.nombres=Entry(marco,width=25)
        self.nombres.grid(row=1, column=1, padx=10, pady=8)

        label_correo=Label(marco,text="Correo electronico: ",font=("Comic Sans", 10,"bold")).grid(row=2,column=0,sticky='s',padx=10,pady=8)
        self.correo=Entry(marco,width=25)
        self.correo.grid(row=2, column=1, padx=10, pady=8)

        label_password=Label(marco,text="Contraseña: ",font=("Comic Sans", 10,"bold")).grid(row=3,column=0,sticky='s',padx=10,pady=8)
        self.password=Entry(marco,width=25,show="*")
        self.password.grid(row=3, column=1, padx=10, pady=8)

        label_password=Label(marco,text="Repetir contraseña: ",font=("Comic Sans", 10,"bold")).grid(row=4,column=0,sticky='s',padx=10,pady=8)
        self.repetir_password=Entry(marco,width=25,show="*")
        self.repetir_password.grid(row=4, column=1, padx=10, pady=8)
        
        "--------------- Marco pregunta --------------------"
        marco_pregunta = LabelFrame(ventana, text="Si olvidas tu contraseña",font=("Comic Sans", 10,"bold"),pady=10)
        marco_pregunta.config(bd=2,pady=5)
        marco_pregunta.pack()

        "--------------- Pregunta --------------------"
        label_pregunta=Label(marco_pregunta,text="Pregunta: ",font=("Comic Sans", 10,"bold")).grid(row=0,column=0,sticky='s',padx=10,pady=8)
        self.combo_pregunta=ttk.Combobox(marco_pregunta,values=["¿Nombre de tu primera mascota?","¿Lugar dónde fuiste al colegio?","¿En que ciudad naciste?","¿Cómo se llama tu equipo favorito?"], width=30,state="readonly")
        self.combo_pregunta.current(0)
        self.combo_pregunta.grid(row=0,column=1,padx=10,pady=8)
  
        label_respuesta=Label(marco_pregunta,text="Respuesta: ",font=("Comic Sans", 10,"bold")).grid(row=1,column=0,sticky='s',padx=10,pady=8)
        self.respuesta=Entry(marco_pregunta,width=33)
        self.respuesta.grid(row=1, column=1, padx=10, pady=8)        
        
        label_nota=Label(marco_pregunta,text="*Esta respuesta te permitira recuperar tu contraseña.",font=("Comic Sans", 9,"bold"),foreground="blue").grid(row=2,column=0,columnspan=2,sticky='s',padx=10)

        "--------------- Frame botones --------------------"
        frame_botones=Frame(ventana)
        frame_botones.pack()

        "--------------- Botones --------------------"
        boton_registrar=Button(frame_botones,text="REGISTRAR",command=self.Registrar_usuario ,height=2,width=10,bg="green",fg="white",font=("Comic Sans", 10,"bold")).grid(row=0, column=1, padx=10, pady=15)
        boton_limpiar=Button(frame_botones,text="LIMPIAR",command=self.Limpiar_formulario ,height=2,width=10,bg="gray",fg="white",font=("Comic Sans", 10,"bold")).grid(row=0, column=2, padx=10, pady=15)
        boton_cancelar=Button(frame_botones,text="CERRAR",command=self.LLamar_login ,height=2,width=10,bg="red",fg="white",font=("Comic Sans", 10,"bold")).grid(row=0, column=3, padx=10, pady=15)
        

    def Limpiar_formulario(self):
        self.dni.delete(0, END)
        self.nombres.delete(0, END)
        self.correo.delete(0, END)
        self.password.delete(0, END)
        self.repetir_password.delete(0, END)
        self.combo_pregunta.delete(0, END)
        self.respuesta.delete(0, END)
    
    #call registro              
    def LLamar_login(self):
        ventana.destroy()    
        subprocess.call(['python',self.ruta_script_login])


    def Registrar_usuario(self):
        if self.Validar_formulario_completo() and self.Validar_contraseña() and self.Validar_dni():
            query='INSERT INTO Usuarios VALUES(NULL, ?, ?, ?, ?, ?)'
            parameters = (self.dni.get(),self.nombres.get(),self.correo.get(),self.password.get(),self.respuesta.get())
            self.Ejecutar_consulta(query, parameters)
            self.createTable()
            messagebox.showinfo("REGISTRO EXITOSO", f'Bienvenido {self.nombres.get()}')
            print('USUARIO CREADO')
            self.Limpiar_formulario()
            

    def Ejecutar_consulta(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conexion:
            cursor=conexion.cursor()
            result=cursor.execute(query,parameters)
            conexion.commit()
        return result 
    
 
    def createTable(self,dni):
        self.dni=dni
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        table_name = f"TABLA_{self.dni}"
        # Verificar si la tabla ya existe
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        existing_table = cursor.fetchone()
        if existing_table is None:
            # La tabla no existe, entonces la creamos
            cursor.execute(
                f"""CREATE TABLE {table_name} (
                    ID integer PRIMARY KEY AUTOINCREMENT,
                    PAGINA varchar UNIQUE,
                    CONTRASEÑA varchar
                )"""
            )
            conn.commit()
        conn.close()


        
    def Validar_formulario_completo(self):
        if len(self.dni.get()) !=0 and len(self.nombres.get()) !=0 and len(self.password.get()) !=0 and len(self.repetir_password.get()) !=0 and len(self.correo.get()) !=0 and len(self.respuesta.get()) !=0:
            return True
        else:
             messagebox.showerror("ERROR EN REGISTRO", "Complete todos los campos del formulario")
    def Validar_contraseña(self):
        if(str(self.password.get()) == str(self.repetir_password.get())):
            return True
        else:
            messagebox.showerror("ERROR EN REGISTRO", "Contraseñas no coinciden")
 
    def Buscar_dni(self, dni):
        with sqlite3.connect(self.db_name) as conexion:
            cursor=conexion.cursor()
            sql="SELECT * FROM Usuarios WHERE DNI = {}".format(dni)
            cursor.execute(sql)
            dnix= cursor.fetchall() # obtener respuesta como lista
            cursor.close()
            return dnix
    
    def Validar_dni(self):
        dni= self.dni.get()
        dato = self.Buscar_dni(dni)
        if (dato == []):
            return True
        else:
            messagebox.showerror("ERROR EN REGISTRO", "DNI registrado anteriormente")

    

    
if __name__ == '__main__':
    ventana=Tk()
    application=Registro(ventana)
    ventana.mainloop()