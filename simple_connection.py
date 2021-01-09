import os

from flask import Flask, render_template, render_template_string, request, Response
from dotenv import load_dotenv
import pymysql

load_dotenv()

app = Flask(__name__)

@app.route('/', methods=["GET"])
def index():
    # establecer conexión
    db = pymysql.connect(
        host='localhost',
        user='pentaho_user',
        password=str(os.getenv("PASSWORD")),
        db='dbg'
    )
    cur = db.cursor()

    # sql principal
    sql = "SELECT * FROM datacator.municipios"

    # filtro y orden --- PENDIENTE CAMBIAR EL TIPO DE VALOR (INT, FLOAT, DATA) y NO ENVIAR VALORES EN BLANCO
    whereSQL = ""
    sortSQL = ""
    for key, value in request.args.items():
        if value != "":
            if key == "sort1" or key == "sort2" or key == "sort3":
                if sortSQL == "":
                    sortSQL = " ORDER BY "
                else:
                    sortSQL = sortSQL + ", "
                sortSQL = sortSQL + value
            elif key != "step" and key != "page": #pendiente implementar paginacion
                if whereSQL == "":
                    whereSQL = " WHERE "
                else:
                    whereSQL = whereSQL + " AND "
                if '%' in value:
                    whereSQL = whereSQL + key + " like '" + value + "'"
                else:
                    whereSQL = whereSQL + key + " = '" + value + "'"
    sql = sql + whereSQL + sortSQL

    # ejecutar consulta
    cur.execute(sql)
    colnames = [desc[0] for desc in cur.description]
    cecos = cur.fetchall()
    cur.close()

    # paginación

    # enviar datos a plantilla
    return render_template('simple_table.html',table=cecos, colnames=colnames, params=request.args)

@app.route('/csv/', methods=["GET"])
def csv():
    # establecer conexión
    db = pymysql.connect(
        host='localhost',
        user='pentaho_user',
        password=str(os.getenv("PASSWORD")),
        db='dbg'
    )
    cur = db.cursor()

    # sql principal
    sql = "SELECT * FROM datacator.municipios"

    # filtro y orden --- PENDIENTE CAMBIAR EL TIPO DE VALOR (INT, FLOAT, DATA) y NO ENVIAR VALORES EN BLANCO
    whereSQL = ""
    sortSQL = ""
    for key, value in request.args.items():
        if value != "":
            if key == "sort1" or key == "sort2" or key == "sort3":
                if sortSQL == "":
                    sortSQL = " ORDER BY "
                else:
                    sortSQL = sortSQL + ", "
                sortSQL = sortSQL + value
            elif key != "step" and key != "page":
                if whereSQL == "":
                    whereSQL = " WHERE "
                else:
                    whereSQL = whereSQL + " AND "
                if '%' in value:
                    whereSQL = whereSQL + key + " like '" + value + "'"
                else:
                    whereSQL = whereSQL + key + " = '" + value + "'"
    sql = sql + whereSQL + sortSQL

    # ejecutar consulta
    cur.execute(sql)
    colnames = [desc[0] for desc in cur.description]
    cecos = cur.fetchall()
    cur.close()

    # Generar response
    response = Response(u'\uFEFF' + render_template('simple_table_csv.html',table=cecos, colnames=colnames, params=request.args))
    response.headers['Content-disposition'] = 'attachment; filename=download.csv'
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'

    return response

if __name__ == '__main__':
    app.run()
