import os

from flask import Flask, render_template, request
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

    # filtro
    whereSQL = ""
    for key, value in request.args.items():
        if key != "sort" and value != "":
            if whereSQL == "":
                whereSQL = " WHERE "
            else:
                whereSQL = whereSQL + " AND "
            if '%' in value:
                whereSQL = whereSQL + key + " like '" + value + "'"
            else:
                whereSQL = whereSQL + key + " = '" + value + "'"
    sql = sql + whereSQL

    # orden
    if request.method == 'GET':
        sort = request.args.get('sort')
        if sort:
            sql = sql + ' ORDER BY ' + sort

    print(sql)

    # ejecutar consulta
    cur.execute(sql)
    colnames = [desc[0] for desc in cur.description]
    cecos = cur.fetchall()

    # exportar


    # paginación

    # enviar datos a plantilla
    return render_template('simple_table.html',table=cecos, colnames=colnames, params=request.args)

if __name__ == '__main__':
    app.run()
