import sqlite3

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
            sql= "SELECT * FROM Usuarios WHERE DNI = ? AND CONTRASEÑA = ?"
            cursor.execute(sql, (self.dni, self.password))
            validacion= cursor.fetchall() # obtener respuesta como lista
            cursor.close()
            return validacion