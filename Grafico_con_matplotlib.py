import os
import base64
from io import BytesIO

from flask import Flask, render_template
from matplotlib.figure import Figure
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config.update(
    TESTING=False,
    FLASK_ENV='development',
    DEBUG=True
)

app.config['FLASK_ENV'] = 'development'

@app.route('/')
def grafico():
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    ax.plot([1, 2])
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"

if __name__ == '__main__':
    app.run()
