from flask import Flask, request, render_template, url_for, redirect
import sqlite3

app = Flask(__name__)

#Creacion de la base de datos segun estructura 
def init_database():
    #Creamos la base de datos o se conecta si ya existe
    conn = sqlite3.connect("citas.db")

    
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS pacientes(
          id INTEGER PRIMARY KEY,
          mascota TEXT NOT NULL,
          propietario TEXT NOT NULL,
          especie TEXT NOT NULL,
          fecha DATE NOT NULL 
        )
        """
        
    )
    conn.commit()
    conn.close()
 
 #inicializa la cracion de la base de datos    
init_database()


@app.route("/")
def agenda():
    #conexion a la base de datos 
    conn = sqlite3.connect("citas.db")
    #Permite manejar lo sregistros en forma de diccionario
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pacientes")
    pacientes = cursor.fetchall()
    
    return render_template("index.html", citas = pacientes)

# Para agendar o crear una cita
@app.route('/agendar', methods=('GET', 'POST'))
def agendar():
    if request.method == 'POST':
        # Obtenemos los datos del formulario
        mascota = request.form['mascota']
        propietario = request.form['propietario']
        especie = request.form['especie']
        fecha = request.form['fecha']
        #Nos conectamos a la base de datos
        conn = sqlite3.connect('citas.db')
        cursor = conn.cursor()
        # Insertamos en la base de datos
        cursor.execute("""
            INSERT INTO pacientes (mascota, propietario, especie, fecha) VALUES (?, ?, ?, ?)
        """, (mascota, propietario, especie, fecha))
        conn.commit()
        conn.close()
        # redirigimos a la raiz
        return redirect("/")
    return render_template('agendar.html')


# @app.route("/create")
# def create():
#     return render_template('create.html')

# @app.route("/save", methods=['POST'])
# def save():
#     mascota = request.form['mascota']
#     propietario = request.form['propietario']
#     especie TEXTquest.form['especie'] 
#     conn = sqlite3.connect("kardex.db")
#     cursor = conn.cursor()
#     cursor.execute(
#         """
#         INSERT INTO pacientes (mascota,propietario,especiTEXT     VALUES (?,?,?)
#         """,
#         (mascota,propietario,especiTEXT )
#     conn.commit()
#     conn.close()
#     return redirect('/')


# @app.route("/edit/<int:id>")
# def persona_edit(id):
#     #conexion a la base de datos 
#     conn = sqlite3.connect("kardex.db")
#     #Permite manejar lo sregistros en forma de diccionario
#     conn.row_factory = sqlite3.Row
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM pacientes WHERE id = ?", (id,))
#     persona = cursor.fetchone()
#     conn.close()
#     return render_template('edit.html', persona = persona)

# @app.route("/update", methods=['POST'])
# def persona_update():
#     id = request.form['id']
#     mascota = request.form['mascota']
#     propietario = request.form['propietario']
#     especie TEXTquest.form['especie'TEXT   #conexion a la base de datos 
#     conn = sqlite3.connect("kardex.db")
#     cursor = conn.cursor()
    
#     cursor.execute("UPDATE pacientes SET mascota=?,propietario=?,especie=TEXTERE id=?", (mascota,propietario,especie,TEXT
#     conn.commit()
#     conn.close()
#     return redirect('/')

# @app.route("/delete/<int:id>")
# def persona_delete(id):
#     conn = sqlite3.connect("kardex.db")
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM pacientes WHERE id=?", (id,))
#     conn.commit()
#     conn.close()
#     return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)