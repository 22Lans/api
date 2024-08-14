from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
from datetime import time
# initializations
app = Flask(__name__)
CORS(app)

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'bibrpdjqpsjsoq3u5r4n-mysql.services.clever-cloud.com' 
app.config['MYSQL_USER'] = 'uawyrmj9s2gtu8zy'
app.config['MYSQL_PASSWORD'] = 'jW42Eh3kyRSNEnJDxCmU'
app.config['MYSQL_DB'] = 'bibrpdjqpsjsoq3u5r4n'
mysql = MySQL(app)

app.secret_key = "mysecretkey"


@app.route('/login', methods=['POST'])
def login():
    try:
        correo = request.json['correo']
        password = request.json['password']
        
        
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE correo = %s AND password = %s', (correo, password))
        usuario = cur.fetchone()
        cur.close()

        if usuario:
            
            content = {
                'id': usuario[0],
                'nombre': usuario[1],
                'correo': usuario[2],
                'carrera': usuario[3],
                'password': usuario[4],
                'rol': usuario[5]
            }
            return jsonify({'success': True, 'usuario': content})
        else:
           
            return jsonify({'success': False, 'message': 'Correo o contraseña incorrectos'})
    except Exception as e:
        print(f'Error en /login: {e}')  
        return jsonify({'success': False, 'message': str(e)})

@app.route('/register', methods=['POST'])
def register():
    try:
        id = request.json['id']
        nombre = request.json['nombre']
        correo = request.json['correo']
        carrera = request.json['carrera']
        password = request.json['password']
        rol = 'estudiante'

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO usuarios (id, nombre, correo, carrera, password, rol)
            VALUES (%s,%s, %s, %s, %s, %s)
        """, (id, nombre, correo, carrera, password, rol))
        mysql.connection.commit()
        cur.close()

        return jsonify({"success": True, "message": "Usuario registrado exitosamente"})
    except Exception as e:
        print(f'Error en /register: {e}')
        return jsonify({"success": False, "message": str(e)})
    
# ruta para consultar todos los registros
@app.route('/getAll', methods=['GET'])
def getAll():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios')
        rv = cur.fetchall()
        cur.close()
        payload = []
        content = {}
        for result in rv:
            content = {'id': result[0], 'nombre': result[1], 'correo': result[2], 'carrera': result[3], 'password': result[4], 'rol': result[5]}
            payload.append(content)
            content = {}
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion": e})

  

@app.route('/getAllById/<id>',methods=['GET'])
def getAllById(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE id = %s', (id,))
        rv = cur.fetchall()
        cur.close()
        payload = []
        content = {}
        for result in rv:
            content = {'id': result[0], 'nombre': result[1], 'correo': result[2], 'carrera': result[3], 'password': result[4], 'rol': result[5]}
            payload.append(content)
            content = {}
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion": e})
    

@app.route('/update/<id>', methods=['PUT'])
def update_user(id):
    try:
        data = request.json
        nombre = data.get('nombre')
        correo = data.get('correo')
        carrera = data.get('carrera')
        rol = data.get('rol')

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE usuarios
            SET nombre = %s, correo = %s, carrera = %s, rol = %s
            WHERE id = %s
        """, (nombre,  correo, carrera, rol, id))
        mysql.connection.commit()
        cur.close()

        return jsonify({"success": True, "message": "Usuario actualizado"})
    except Exception as e:
        print(f'Error en /update/{id}: {e}')
        return jsonify({"success": False, "message": str(e)})

@app.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM usuarios WHERE id = %s', (id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({"success": True, "message": "Registro eliminado"})
    except Exception as e:
        print(f'Error en /delete/{id}: {e}')
        return jsonify({"success": False, "message": str(e)})


@app.route('/update/<id>', methods=['PUT'])
def update_contact(id):
    try:
        nombre = request.json['nombre']
        correo = request.json['correo']
        carrera = request.json['carrera']
        rol = request.json['rol']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE usuarios
        SET nombre = %s, correo = %s, carrera = %s, rol = %s
        WHERE id = %s
        """, (nombre, correo, carrera, rol, id))
        mysql.connection.commit()
        cur.close()
        return jsonify({"informacion": "Registro actualizado"})
    except Exception as e:
        print(e)
        return jsonify({"informacion": e})



def delete_contact(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM usuarios WHERE id = %s', (id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({"informacion": "Registro eliminado"})
    except Exception as e:
        print(e)
        return jsonify({"informacion": e})


@app.route('/disponibilidad', methods=['POST'])
def save_disponibilidad():
    try:
        data = request.json
        profesor_id = data['profesor_id']
        dia_semana = data['dia_semana']
        hora_inicio = data['hora_inicio']
        hora_fin = data['hora_fin']
        lugar = data['lugar']

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO disponibilidad (profesor_id, dia_semana, hora_inicio, hora_fin, lugar)
            VALUES (%s, %s, %s, %s, %s)
        """, (profesor_id, dia_semana, hora_inicio, hora_fin, lugar))
        mysql.connection.commit()
        cur.close()

        return jsonify({"success": True, "message": "Disponibilidad guardada exitosamente"})
    except Exception as e:
        print(f'Error en /disponibilidad: {e}')
        return jsonify({"success": False, "message": str(e)})

@app.route('/disponibilidad/<int:profesor_id>', methods=['GET'])
def get_disponibilidad(profesor_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM disponibilidad WHERE profesor_id = %s', (profesor_id,))
        disponibilidades = cur.fetchall()
        cur.close()

        payload = []
        for d in disponibilidades:
            payload.append({
                'dia_semana': d[2],
                'hora_inicio': str(d[3]),
                'hora_fin': str(d[4]),
                'lugar': d[5]
            })

        return jsonify(payload)
    except Exception as e:
        print(f'Error en /disponibilidad/{profesor_id}: {e}')
        return jsonify({"success": False, "message": str(e)})
    
@app.route('/getdocente', methods=['GET'])
def getdocente():
    try:
        query = request.args.get('query', '')
        cur = mysql.connection.cursor()
        if query:
            cur.execute("SELECT * FROM usuarios WHERE rol = 'docente' AND (nombre LIKE %s )", (f'%{query}%'))
        else:
            cur.execute("SELECT * FROM usuarios WHERE rol = 'docente'")
        rv = cur.fetchall()
        cur.close()
        payload = []
        for result in rv:
            content = {
                'id': result[0],
                'nombre': result[1],
                'correo': result[2],
                'carrera': result[3],
                'password': result[4],
                'rol': result[5]
            }
            payload.append(content)
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion": e})
    
@app.route('/tutoria', methods=['POST'])
def save_tutoria():
    try:
        data = request.json
        estudiante_id = data['estudiante_id']
        profesor_id = data['profesor_id']  # Usa profesor_id aquí
        dia_semana = data['dia_semana']
        hora_inicio = data['hora_inicio']
        hora_fin = data['hora_fin']
        lugar = data['lugar']
        tema = data['tema']

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO tutorias (estudiante_id, profesor_id, dia_semana, hora_inicio, hora_fin, lugar, tema)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (estudiante_id, profesor_id, dia_semana, hora_inicio, hora_fin, lugar, tema))
        mysql.connection.commit()
        cur.close()

        return jsonify({"success": True, "message": "Tutoria solicitada exitosamente"})
    except Exception as e:
        print(f'Error en /tutoria: {e}')
        return jsonify({"success": False, "message": str(e)})


@app.route('/count_users', methods=['GET'])
def count_users():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) FROM usuarios")
        users_count = cur.fetchone()[0]
        cur.close()
        return jsonify({'count': users_count})
    except Exception as e:
        print(f'Error en /count_users: {e}')
        return jsonify({'error': str(e)})

@app.route('/count_tutorias', methods=['GET'])
def count_tutorias():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) FROM tutorias")
        tutorias_count = cur.fetchone()[0]
        cur.close()
        return jsonify({'count': tutorias_count})
    except Exception as e:
        print(f'Error en /count_tutorias: {e}')
        return jsonify({'error': str(e)})

@app.route('/count_users_by_role', methods=['GET'])
def count_users_by_role():
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT rol, COUNT(*) as count
            FROM usuarios
            GROUP BY rol
        """)
        results = cur.fetchall()
        cur.close()

        
        counts = {'admin': 0, 'docente': 0, 'estudiante': 0}
        for result in results:
            role, count = result
            if role in counts:
                counts[role] = count

        return jsonify(counts)
    except Exception as e:
        print(f'Error en /count_users_by_role: {e}')
        return jsonify({'error': str(e)})


@app.route('/tutorias/<int:estudiante_id>', methods=['GET'])
def get_tutorias(estudiante_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT t.*, u.nombre AS profesor_nombre
            FROM tutorias t
            JOIN usuarios u ON t.profesor_id = u.id
            WHERE t.estudiante_id = %s
        """, (estudiante_id,))
        tutorias = cur.fetchall()
        cur.close()

        payload = []
        for tutoria in tutorias:
            payload.append({
                'id': tutoria[0],  # Asegúrate de que 'id' se incluye aquí
                'profesor_nombre': tutoria[9],
                'dia_semana': tutoria[3],
                'hora_inicio': str(tutoria[4]),
                'hora_fin': str(tutoria[5]),
                'lugar': tutoria[6],
                'tema': tutoria[7],
                'estado': tutoria[8]
            })

        return jsonify(payload)
    except Exception as e:
        print(f'Error en /tutorias/{estudiante_id}: {e}')
        return jsonify({"success": False, "message": str(e)})

@app.route('/tutoria/<int:tutoria_id>', methods=['DELETE'])
def delete_tutoria(tutoria_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM tutorias WHERE id = %s', (tutoria_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({"success": True, "message": "Tutoria eliminada exitosamente"})
    except Exception as e:
        print(f'Error en /tutoria/{tutoria_id}: {e}')
        return jsonify({"success": False, "message": str(e)})

@app.route('/tutorias_profesor/<int:profesor_id>', methods=['GET'])
def get_tutorias_profesor(profesor_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT t.*, u.nombre AS estudiante_nombre
            FROM tutorias t
            JOIN usuarios u ON t.estudiante_id = u.id
            WHERE t.profesor_id = %s
        """, (profesor_id,))
        tutorias = cur.fetchall()
        cur.close()

        payload = []
        for tutoria in tutorias:
            payload.append({
                'id': tutoria[0],  # Asegúrate de que 'id' se incluye aquí
                'estudiante_id': tutoria[1],
                'estudiante_nombre': tutoria[9],
                'dia_semana': tutoria[3],
                'hora_inicio': str(tutoria[4]),
                'hora_fin': str(tutoria[5]),
                'lugar': tutoria[6],
                'tema': tutoria[7],
                'estado': tutoria[8]
            })

        return jsonify(payload)
    except Exception as e:
        print(f'Error en /tutorias_profesor/{profesor_id}: {e}')
        return jsonify({"success": False, "message": str(e)})

@app.route('/tutoria/<int:id>', methods=['PUT'])
def update_tutoria(id):
    try:

        nuevo_estado = request.json.get('estado')
        
        if not nuevo_estado:
            return jsonify({"success": False, "message": "Estado no proporcionado"}), 400
        
        cur = mysql.connection.cursor()
        

        cur.execute("SELECT * FROM tutorias WHERE id = %s", (id,))
        tutoria = cur.fetchone()
        if not tutoria:
            cur.close()
            return jsonify({"success": False, "message": "Tutoría no encontrada"}), 404
        
        cur.execute("""
            UPDATE tutorias
            SET estado = %s
            WHERE id = %s
        """, (nuevo_estado, id))
        mysql.connection.commit()
        cur.close()
        
        return jsonify({"success": True, "message": "Estado de tutoría actualizado exitosamente"}), 200
    except Exception as e:
        print(f'Error en /tutoria/{id}: {e}')
        return jsonify({"success": False, "message": str(e)})
    
@app.route('/estudiante_carrera/<int:estudiante_id>', methods=['GET'])
def get_estudiante_carrera(estudiante_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT carrera FROM usuarios WHERE id = %s", (estudiante_id,))
        carrera = cur.fetchone()
        cur.close()

        if carrera:
            return jsonify({'carrera': carrera[0]})
        else:
            return jsonify({'success': False, 'message': 'Estudiante no encontrado'})
    except Exception as e:
        print(f'Error en /estudiante_carrera/{estudiante_id}: {e}')
        return jsonify({"success": False, "message": str(e)})
    
@app.route('/tutoriascompletadas', methods=['POST'])
def save_tutoria_completada():
    try:
        data = request.json
        docente_nombre = data['docente_nombre']
        carrera_docente = data['carrera_docente']
        estudiante_nombre = data['estudiante_nombre']
        estudiante_id = data['estudiante_id']
        tema = data['tema']
        carrera_estudiante = data['carrera_estudiante']
        modulo = data['modulo']
        lugar = data['lugar']
        fecha = data['fecha']
        hora_fin = data['hora_fin']

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO tutoriascompletadas (
                docente_nombre, carrera_docente, estudiante_nombre, estudiante_id,
                tema, carrera_estudiante, modulo, lugar, fecha, hora_fin
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (docente_nombre, carrera_docente, estudiante_nombre, estudiante_id,
              tema, carrera_estudiante, modulo, lugar, fecha, hora_fin))
        mysql.connection.commit()
        cur.close()

        return jsonify({"success": True, "message": "Tutoría completada registrada exitosamente"})
    except Exception as e:
        print(f'Error en /tutoriascompletadas: {e}')
        return jsonify({"success": False, "message": str(e)}), 500
    

@app.route('/tutorias_finalizadas', methods=['POST'])
def get_tutorias_finalizadas():
    try:
        data = request.json
        profesor_nombre = data['profesor_nombre']

        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT docente_nombre, carrera_docente, estudiante_nombre, estudiante_id, tema, carrera_estudiante, modulo, lugar, fecha, hora_fin
            FROM tutoriascompletadas
            WHERE docente_nombre = %s
        """, (profesor_nombre,))
        tutorias = cur.fetchall()
        cur.close()

        payload = []
        for tutoria in tutorias:
            payload.append({
                'docente_nombre': tutoria[0],
                'carrera_docente': tutoria[1],
                'estudiante_nombre': tutoria[2],
                'estudiante_id': tutoria[3],
                'tema': tutoria[4],
                'carrera_estudiante': tutoria[5],
                'modulo': tutoria[6],
                'lugar': tutoria[7],
                'fecha': str(tutoria[8]),  # Convertir la fecha a cadena de texto
                'hora_fin': str(tutoria[9])  # Convertir la hora_fin a cadena de texto
            })

        return jsonify({"success": True, "tutorias": payload})
    except Exception as e:
        print(f'Error en /tutorias_finalizadas: {e}')
        return jsonify({"success": False, "message": str(e)}), 500
    

# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)

