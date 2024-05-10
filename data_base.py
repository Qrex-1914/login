import sqlite3 as sql


db_name='database_proyecto.db'
tabla='Usuarios'

def createDB():
    conn = sql.connect(db_name)
    conn.commit()
    conn.close()


db_name='database_proyecto.db'
tabla_name="users"

def createTable():
    conn=sql.connect(db_name)
    cursor= conn.cursor()
    cursor.execute(
         f"""CREATE TABLE {tabla} (
            ID integer PRIMARY KEY AUTOINCREMENT,
            DNI integer UNIQUE,
            NOMBRE varchar,
            EMAIL varchar,
            CONTRASEÑA varchar,
            RESPUESTA varchar
        )"""

    )
    conn.commit()
    conn.close()


#la parte de PRIMARY KEY es para que no se repita algo por ejemplo ID o un codigo de producto
# si no quiero estar digitando y quiero que sea una enumeracion secuencial puedo colocar PRYMARY KEY AUTOINCREMENT
#nota2: UNIQUE es si quiero que un campo de una columna no se repita no es un PRIMARY KEY, solo es para que no se repita
def insertRow(nombre, followers, subs):
    conn=sql.connect(db_name)
    cursor= conn.cursor()
    instruccion= f"INSERT INTO streamers VALUES ('{nombre}', {followers}, {subs})"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()

def readRows():
    conn=sql.connect(db_name)
    cursor= conn.cursor()
    instruccion= f"SELECT * FROM streamers "
    cursor.execute(instruccion)
    datos= cursor.fetchall()
    conn.commit()
    conn.close()
    print(datos)

def insertRows(lista):
    conn=sql.connect(db_name)
    cursor= conn.cursor()
    instruccion= f"INSERT INTO streamers VALUES (?, ?, ?)"
    cursor.executemany(instruccion,lista)
    conn.commit()
    conn.close()

lista_streamers=[
    ("ender", 20, 4),
    ("viena", 30, 3),
    ("shadit", 40, 2)

] # esta estructura es la de salida de la base de datos, nosotros damos la misma
#forma para poder ingresar varios

def readOrdered(field):
    conn=sql.connect(db_name)
    cursor= conn.cursor()
    instruccion= f"SELECT * FROM streamers ORDER BY {field} " #<-asi ordena de menor a mayor, si quieres alrevez metele DESC a lo ultimo
    cursor.execute(instruccion)
    datos= cursor.fetchall()
    conn.commit()
    conn.close()
    print(datos)

def search():
    conn=sql.connect(db_name)
    cursor= conn.cursor()
    instruccion= f"SELECT * FROM streamers WHERE name like 'js' "
    cursor.execute(instruccion)
    datos= cursor.fetchall()
    conn.commit()
    conn.close()
    print(datos)

#nota: si es numero no lleva estas comillas '', si quieres que sea no sensitive en vez de igual colocas like, si no sabes todo el nombre el simbolo % significa * en linux

def updateFields():
    conn=sql.connect(db_name)
    cursor= conn.cursor()
    instruccion= f"UPDATE streamers SET followers = 60 WHERE name like 'js' "
    cursor.execute(instruccion)
    conn.commit()
    conn.close()

def deleteRow():
    conn=sql.connect(db_name)
    cursor= conn.cursor()
    instruccion= f"DELETE FROM streamers WHERE name like 'ibai'"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    createDB()
    createTable()
    #insertRow("Ibai", 700000, 25000)
    #insertRow("js", 10, 0)
    #readRows() # esto devuelve una lista [] y dentro tenemos tuplas ()
    #insertRows(lista_streamers)
    #readOrdered("subs")
    #search()
    #updateFields()
    #deleteRow()
    pass