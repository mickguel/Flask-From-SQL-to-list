import os

from flask import Flask, render_template, request
from dotenv import load_dotenv
import pymysql

load_dotenv()

app = Flask(__name__)

@app.route('/', methods=["GET"])
def index():
    db = pymysql.connect(
        host='localhost',
        user='pentaho_user',
        password=str(os.getenv("PASSWORD")),
        db='dbg'
    )
    sql = "SELECT * FROM datacator.municipios"
    if request.method == 'GET':
        sort = request.args.get('sort')
        print(sort)
        if sort:
            sql = sql + ' ORDER BY ' + sort
    cur = db.cursor()
    cur.execute(sql)
    colnames = [desc[0] for desc in cur.description]
    cecos = cur.fetchall()
    #return str (str(cur.description) + str(cecos))
    #print(colnames)
    return render_template('simple_table.html',table=cecos, colnames=colnames)

if __name__ == '__main__':
    app.run()
