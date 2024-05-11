from tkinter import *
from tkinter import ttk
from tkinter import messagebox 
from db import DatabaseManager
from Login import create_login_interface

#verificar si el modulo ha sido ejecutado correctamente  
if __name__ == '__main__':
    ventana_login=Tk()
    db_manager=DatabaseManager()
    application=create_login_interface(ventana_login,db_manager)
    ventana_login.mainloop()