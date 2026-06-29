from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def crear_bd():
    conexion = sqlite3.connect('alumnos.db')
    cursor = conexion.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alumnos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matricula TEXT,
            nombre TEXT,
            apellido_paterno TEXT,
            apellido_materno TEXT,
            edad INTEGER,
            semestre TEXT,
            grupo TEXT,
            carrera TEXT,
            correo TEXT
        )
    ''')

    conexion.commit()
    conexion.close()

crear_bd()


@app.route('/')
def inicio():
    conexion = sqlite3.connect('alumnos.db')
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM alumnos")
    alumnos = cursor.fetchall()

    conexion.close()

    return render_template('index.html', alumnos=alumnos)


@app.route('/agregar', methods=['GET', 'POST'])
def agregar():

    if request.method == 'POST':

        datos = (
            request.form['matricula'],
            request.form['nombre'],
            request.form['apellido_paterno'],
            request.form['apellido_materno'],
            request.form['edad'],
            request.form['semestre'],
            request.form['grupo'],
            request.form['carrera'],
            request.form['correo']
        )

        conexion = sqlite3.connect('alumnos.db')
        cursor = conexion.cursor()

        cursor.execute('''
            INSERT INTO alumnos(
            matricula,nombre,apellido_paterno,
            apellido_materno,edad,semestre,
            grupo,carrera,correo)
            VALUES (?,?,?,?,?,?,?,?,?)
        ''', datos)

        conexion.commit()
        conexion.close()

        return redirect(url_for('inicio'))

    return render_template('agregar.html')


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):

    conexion = sqlite3.connect('alumnos.db')
    cursor = conexion.cursor()

    if request.method == 'POST':

        cursor.execute('''
            UPDATE alumnos SET
            matricula=?,
            nombre=?,
            apellido_paterno=?,
            apellido_materno=?,
            edad=?,
            semestre=?,
            grupo=?,
            carrera=?,
            correo=?
            WHERE id=?
        ''',
        (
            request.form['matricula'],
            request.form['nombre'],
            request.form['apellido_paterno'],
            request.form['apellido_materno'],
            request.form['edad'],
            request.form['semestre'],
            request.form['grupo'],
            request.form['carrera'],
            request.form['correo'],
            id
        ))

        conexion.commit()
        conexion.close()

        return redirect(url_for('inicio'))

    cursor.execute("SELECT * FROM alumnos WHERE id=?", (id,))
    alumno = cursor.fetchone()

    conexion.close()

    return render_template('editar.html', alumno=alumno)


@app.route('/eliminar/<int:id>')
def eliminar(id):

    conexion = sqlite3.connect('alumnos.db')
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM alumnos WHERE id=?", (id,))

    conexion.commit()
    conexion.close()

    return redirect(url_for('inicio'))


if __name__ == '__main__':
    app.run(debug=True)