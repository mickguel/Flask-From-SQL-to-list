import os
from flask import Flask, render_template
from dotenv import load_dotenv
import pymysql

load_dotenv()

app = Flask(__name__)

app.config.update(
    TESTING=False,
    FLASK_ENV='development',
    DEBUG=True
)

app.config['FLASK_ENV'] = 'development'

@app.route('/')
def index():
    db = pymysql.connect(
        host='localhost',
        user='pentaho_user',
        password=str(os.getenv("PASSWORD")),
        db='dbg'
    )
    cur = db.cursor()
    cur.execute('SELECT * FROM datacator.municipios')
    colnames = [desc[0] for desc in cur.description]
    cecos = cur.fetchall()
    #return str (str(cur.description) + str(cecos))
    #print(colnames)
    return render_template('simple_table.html',table=cecos, colnames=colnames)

if __name__ == '__main__':
    app.run()
