import random
from flask import Flask, render_template, request, session, redirect, url_for
import mysql.connector


# Clase para manejar la base de datos
class BaseDeDatos:
    def __init__(self, host="localhost", user="root", password="", database="ejercicios_db"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def conectar(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )


# Clase para el Par o Impar
class JuegoParImpar:
    def __init__(self, db):
        self.db = db

    def evaluar(self, numero):
        "Evalúa si un número es par o impar"
        if numero % 2 == 0:
            return "Par"
        else:
            return "Impar"

    def guardar_registro(self, numero, resultado):
        "Guarda un registro en la base de datos si no se ha alcanzado el límite de 5."
        conn = self.db.conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM registro_par_impar WHERE resultado = %s", (resultado,))
        total_registrados = cursor.fetchone()[0]

        if total_registrados < 5:
            cursor.execute("INSERT INTO registro_par_impar (numero, resultado) VALUES (%s, %s)", (numero, resultado))
            conn.commit()
            mensaje = f" Número {resultado} guardado correctamente.({total_registrados + 1}/5) en la base de datos."
            
        else:
            mensaje = f" Ya se guardaron los primeros 5 números {resultado} en la base de datos."

        cursor.close()
        conn.close()
        return mensaje

    def obtener_estadisticas(self):
        """Obtiene estadísticas de los registros guardados."""
        conn = self.db.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT resultado, COUNT(*) as total FROM registro_par_impar GROUP BY resultado")
        estadisticas = cursor.fetchall()
        cursor.close()
        conn.close()
        return estadisticas


# Clase para la Tabla de Multiplicar
class TablaMultiplicar:
    def __init__(self, db):
        self.db = db

    def generar_tabla(self, numero):
        """Genera la tabla de multiplicar del 1 al 10."""
        tabla_resultados = []
        for i in range(1, 11):
            tabla_resultados.append({"multiplicador": i, "resultado": numero * i})
        return tabla_resultados

    def guardar_registro(self, numero):
        """Guarda el número de la tabla en la base de datos."""
        conn = self.db.conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO registro_tablas (numero) VALUES (%s)", (numero,))
        conn.commit()
        cursor.close()
        conn.close()


# Clase para Adivina el Número
class JuegoAdivina:
    def __init__(self, db):
        self.db = db

    def evaluar_intento(self, intento, secreto):
        """Evalúa si el número es mayor, menor o correcto."""
        if intento < secreto:
            return "El numero secreto es MAYOR."
        elif intento > secreto:
            return "El numero secreto es MENOR."
        else:
            return "CORRECTO, tas makia"

    def iniciar_juego(self):
        """Inicia un nuevo juego generando número secreto y reiniciando intentos."""
        return {
            "numero_secreto": random.randint(1, 100),
            "intentos": 0
        }

    def procesar_intento(self, intento, session_data):
        """Procesa un intento del usuario."""
        session_data["intentos"] += 1
        secreto = session_data["numero_secreto"]
        pista = self.evaluar_intento(intento, secreto)
        ganado = False

        if intento == secreto:
            ganado = True
            # Guardar partida ganada en MySQL
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO juego_adivina (numero_secreto, intentos_totales) VALUES (%s, %s)",
                (secreto, session_data["intentos"])
            )
            conn.commit()
            cursor.close()
            conn.close()

        return pista, ganado, session_data


# Instancia de la aplicación Flask
app = Flask(__name__)
app.secret_key = "clave_secreta_para_sesion"

# Inicializar la base de datos y los ejercicios
db = BaseDeDatos()
juego_par_impar = JuegoParImpar(db)
tabla_multiplicar = TablaMultiplicar(db)
juego_adivina = JuegoAdivina(db)


@app.route("/")
def index():
    return render_template("index.html")


# Rutas para Par o Impar
@app.route("/par_impar", methods=["GET", "POST"])
def par_impar():
    resultado = None
    mensaje_db = None

    if request.method == "POST":
        numero = int(request.form["numero"])
        resultado = juego_par_impar.evaluar(numero)
        mensaje_db = juego_par_impar.guardar_registro(numero, resultado)

    return render_template("par_impar.html", resultado=resultado, mensaje_db=mensaje_db)


# Rutas para Tabla de Multiplicar
@app.route("/tabla", methods=["GET", "POST"])
def tabla():
    tabla_resultados = []
    numero = None
    if request.method == "POST":
        numero = int(request.form["numero"])
        tabla_resultados = tabla_multiplicar.generar_tabla(numero)
        juego_multiplicar = tabla_multiplicar.guardar_registro(numero)

    return render_template('tabla.html', numero=numero, tabla=tabla_resultados)


# Rutas para Adivina el Número
@app.route("/adivina", methods=["GET", "POST"])
def adivina():
    # Iniciar el juego si no hay número secreto en la sesión
    if "numero_secreto" not in session:
        session_data = juego_adivina.iniciar_juego()
        session["numero_secreto"] = session_data["numero_secreto"]
        session["intentos"] = session_data["intentos"]

    pista = None
    ganado = False

    if request.method == "POST":
        intento = int(request.form["intento"])
        pista, ganado, session_data = juego_adivina.procesar_intento(intento, session)
        # Actualizar la sesión de Flask con los datos actualizados
        session["numero_secreto"] = session_data["numero_secreto"]
        session["intentos"] = session_data["intentos"]

    return render_template("adivina.html", pista=pista, ganado=ganado, intentos=session.get("intentos", 0))


@app.route("/reiniciar_juego")
def reiniciar_juego():
    session.pop("numero_secreto", None)
    session.pop("intentos", None)
    return redirect(url_for("adivina"))


if __name__ == '__main__':
    app.run(debug=True)