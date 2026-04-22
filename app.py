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
    
    return render_template("index.html", pacientes = pacientes)

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


# Para la modificacion de una cita
@app.route('/modificar/<int:id>', methods=('GET', 'POST'))
def modificar(id):
    # Obtenmos los datos de la cita
    conn = sqlite3.connect('citas.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pacientes WHERE id = ?', (id,))
    cita = cursor.fetchone()

    if request.method == 'POST':
        #obtenemos los datos del formulario
        mascota = request.form['mascota']
        propietario = request.form['propietario']
        especie = request.form['especie']
        fecha = request.form['fecha']
        # Ejecución de la actualización (UPDATE) con los nuevos valores
        conn.execute("""
            UPDATE pacientes SET mascota= ?, propietario=?, especie=?, fecha = ? WHERE id = ?
        """, (mascota, propietario, especie, fecha, id))
        conn.commit()
        conn.close()
        return redirect("/")

    conn.close()
    # Renderiza el formulario de edición con la información de la cita seleccionada
    return render_template('modificar.html', cita=cita)

# Para la cancelacion de una cita
@app.route('/cancelar/<int:id>')
def cancelar(id):
    conn = sqlite3.connect("citas.db")
    cursor = conn.cursor()
    # Ejecuatmos la sentencia con cursor para la eliminacin de la cita
    cursor.execute("DELETE FROM pacientes WHERE id=?",(id,))
    conn.commit()
    conn.close()
    # Regresa a la vista de mis citas
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)