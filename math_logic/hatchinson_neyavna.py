import numpy as np
import parser
import os, shutil
import uuid
import matplotlib.pyplot as plt
import numpy as np
from flask import *


class Hatchinson_Neyavna:
    def __init__(self, step, tau, m, T, formula=""): # formula is optional
        self.step = step
        self.tau = tau
        self.m = m
        self.T = T
        self.formula = formula


    def calculate(self):
        t = np.arange(0, self.T + 0.1, self.step)
        x = np.zeros(t.size)
        x[0] = self.fi(0)
        i = 1
        k=0

        while i < t.size:
            if t[i]-self.tau <= 0:
                k = k+ 1
                x[i] = x[i-1] / (1 - self.step * self.m * (1 - self.fi (t[i+1] - self.tau) / 100))
            else:
                x[i] = x[i-1] / (1 - self.step *self.m * (1 - x[i+1-k] / 100))
            i = i + 1
        return t, x

    def fi(self, _x):
        code = parser.expr(self.formula).compile()
        x = _x
        return eval(code)

    def f(self, t, x0, x1):
        return self.m * (1 - x1/100)*x0 # TODO: change 100

    # setter for formula
    def setFormula(self, formula):
        self.formula = formula

    def draw_save(self, app, t, x):
        fig, ax1 = plt.subplots(figsize=(15,5))
        plt.xlabel('x')
        plt.ylabel('t')

        plt.plot(t, x)

        filepath = uuid.uuid4().hex + ".png"
        path = os.path.join(app.root_path, 'static', 'images', filepath)

        folder = os.path.join(app.root_path, 'static', 'images')

        for item in os.listdir(folder):
            file = os.path.join(folder, item)
            try:
                if os.path.isfile(file) or os.path.islink(file):
                    os.unlink(file)
                elif os.path.isdir(file):
                    shutil.rmtree(file)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file, e))

        plt.savefig(path, transparent=True)
        url_png = url_for("static", filename=f'images/{filepath}')
        
        return url_png
        
        
