from flask import Flask, render_template, request, url_for
from flask_bootstrap import Bootstrap
from math_logic.hatchinson_yavna import Hatchinson_Yavna
from math_logic.hatchinson_neyavna import Hatchinson_Neyavna
from math_logic.example import Example
from math_logic.systema import Systema
from math_logic.kermaka import Kermaka
import numpy as np

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('hatchinson_yavna.html')

@app.route('/example')
def example():
    return render_template('example.html')

@app.route('/calculate/example', methods=['POST'])
def calculate_example():
    step = float(request.form['h'])
    method = Example(step)

    t, x, y, x_tochne, y_tochne = method.calculate()

    img_path = method.draw_save(app, t[1:-1], x[1:-1], y[1:-1], x_tochne[1:-1], y_tochne[1:-1])

    x_string = to_str(x)

    t_string = to_str(t)

    obj = {
        'img': img_path,
        't': t_string,
        'x': x_string,
        'length': str(len(t))
        }
    
    return obj

@app.route('/systema')
def systema():
    return render_template('systema.html')

@app.route('/calculate/systema', methods=['POST'])
def calculate_systema():
    step = float(request.form['h'])
    tau_1 = float(request.form['tau_1'])
    tau_2 = float(request.form['tau_2'])
    alpha = float(request.form['alpfa'])
    beta = float(request.form['beta'])
    gama = float(request.form['gama'])
    func_1 = str(request.form['func_1'])
    func_2 = str(request.form['func_2'])
    func_3 = str(request.form['func_3'])

    method = Systema(step, tau_1, tau_2, alpha, beta, gama, func_1, func_2, func_3)

    t, x, y, z = method.calculate()

    img_path = method.draw_save(app, t[1:-1], x[1:-1], y[1:-1], z[1:-1])

    x_string = to_str(x)

    t_string = to_str(t)

    obj = {
        'img': img_path,
        't': t_string,
        'x': x_string,
        'length': str(len(t))
        }
    
    return obj

@app.route('/hatchinson_yavna')
def hatchinson_yavna():
    return render_template('hatchinson_yavna.html')

@app.route('/hatchinson_neyavna')
def hatchinson_neyavna():
    return render_template('hatchinson_neyavna.html')

@app.route('/calculate/hatchinson_yavna', methods=['POST'])
def calculate_hatchinson_yavna():
    step = float(request.form['h'])
    tau = float(request.form['tau'])
    m = float(request.form['m'])
    K = float(request.form['K'])

    formula = str(request.form['func'])
    method = Hatchinson_Yavna(step, tau, m, K, formula)

    t, x = method.calculate()

    img_path = method.draw_save(app, t[1:-1], x[1:-1])

    x_string = to_str(x)

    t_string = to_str(t)

    obj = {
        'img': img_path,
        't': t_string,
        'x': x_string,
        'length': str(len(t))
        }
    
    return obj

@app.route('/calculate/hatchinson_neyavna', methods=['POST'])
def calculate_hatchinson_neyavna():
    step = float(request.form['h'])
    tau = float(request.form['tau'])
    m = float(request.form['m'])
    K = float(request.form['K'])

    formula = str(request.form['func'])
    method = Hatchinson_Neyavna(step, tau, m, K, formula)

    t, x = method.calculate()

    img_path = method.draw_save(app, t[1:-1], x[1:-1])

    x_string = to_str(x)

    t_string = to_str(t)

    obj = {
        'img': img_path,
        't': t_string,
        'x': x_string,
        'length': str(len(t))
        }
    
    return obj

@app.route('/kermaka')
def kermaka():
    return render_template('kermaka.html')

@app.route('/calculate/kermaka', methods=['POST'])
def calculate_kermaka():
    step = float(request.form['h'])
    tau_1 = float(request.form['tau_1'])
    tau_2 = float(request.form['tau_2'])
    func_1 = str(request.form['func_1'])
    func_2 = str(request.form['func_2'])
    func_3 = str(request.form['func_3'])

    method = Kermaka(step, tau_1, tau_2, func_1, func_2, func_3)

    t, x, y, z = method.calculate()

    img_path = method.draw_save(app, t[1:-1], x[1:-1], y[1:-1], z[1:-1])

    x_string = to_str(x)

    t_string = to_str(t)

    obj = {
        'img': img_path,
        't': t_string,
        'x': x_string,
        'length': str(len(t))
        }
    
    return obj

def to_str(var):
    return str(list(np.reshape(np.asarray(var), (1, np.size(var)))[0]))[1:-1]


if __name__ == '__main__':
    app.run()
