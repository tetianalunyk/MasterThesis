import numpy as np
import parser
import os, shutil
import uuid
import matplotlib.pyplot as plt
from flask import *


class Example:
    def __init__(self, step): # formula is optional
        self.step = step

    def calculate(self):
        T=3
        tau = 1
        tau_2 = 2
        k = 0
        t = np.arange(0, 3+2*self.step, self.step)
        x = np.zeros(t.size)
        y = np.zeros(t.size)
        v = np.zeros(t.size)
        u = np.zeros(t.size)
        p = np.zeros(t.size)
        q = np.zeros(t.size)
        x[0] = self.fi(0)
        y[0] = self.psi(0)
        i = 1

        while t[i-1]-tau < 0 and t[i-1] <= T:
                v[i-1] = self.fi(t[i-1]-tau)
                u[i-1] = self.psi(t[i-1]-tau)
                x[i] = x[i-1] + self.step * self.f(t[i-1], x[i-1], y[i-1], self.fi(t[i-1]-tau), self.fi(t[i-1]-tau_2), self.psi(t[i-1]-tau), self.psi(t[i-1]-tau_2))
                y[i] = y[i-1] + self.step * self.g(t[i-1], x[i-1], y[i-1], self.fi(t[i-1]-tau), self.fi(t[i-1]-tau_2), self.psi(t[i-1]-tau), self.psi(t[i-1]-tau_2))
                i = i+1

        while t[i-1]-tau_2 < 0 and t[i-1]<=T:
                k = np.searchsorted(t, t[i-1]-tau)
                k=k+1
                v[i-1] = (t[i-1]-tau-t[k]) / self.step * x[k+1] + (t[k+1]- t[i-1]+tau) / self.step * x[k]
                u[i-1] = (t[i-1]-tau-t[k]) / self.step * y[k+1] + (t[k+1]- t[i-1]+tau) / self.step * y[k]
                x[i] = x[i-1] + self.step * self.f(t[i-1], x[i-1], y[i-1], v[i-1], self.fi(t[i-1]-tau_2), u[i-1], self.psi(t[i-1]-tau_2))
                y[i] = y[i-1] + self.step * self.g(t[i-1], x[i-1], y[i-1], v[i-1], self.fi(t[i-1]-tau_2), u[i-1], self.psi(t[i-1]-tau_2))
                i = i+1

        while t[i-1]<=T:
                k = np.searchsorted(t, t[i-1]-tau, side='left')
                m = np.searchsorted(t, t[i-1]-tau_2, side='left')
                k=k+1
                m=m+1
                v[i-1] = (t[i-1]-tau-t[k]) / self.step * x[k+1] + (t[k+1]- t[i-1]+tau) / self.step * x[k]
                u[i-1] = (t[i-1]-tau-t[k]) / self.step * y[k+1] + (t[k+1]- t[i-1]+tau) / self.step * y[k]
                p[i-1] = (t[i-1]-tau_2-t[m]) / self.step * x[m+1] + (t[m+1]- t[i-1]+tau_2) / self.step * x[m]
                q[i-1] = (t[i-1]-tau_2-t[m]) / self.step * y[m+1] + (t[m+1]- t[i-1]+tau_2) / self.step * y[m]
                x[i] = x[i-1] + self.step * self.f(t[i-1], x[i-1], y[i-1], v[i-1], p[i-1], u[i-1], q[i-1])
                y[i] = y[i-1] + self.step * self.g(t[i-1], x[i-1], y[i-1], v[i-1], p[i-1], u[i-1], q[i-1])
                i = i+1
        print(y)

        x_tochne = np.zeros(t.size)
        y_tochne = np.zeros(t.size)

        i=0
        while t[i]<=1:
            x_tochne[i] = 2 * pow(t[i], 3) + 4 * pow(t[i], 2) - 8 * t[i] + 2
            y_tochne[i] = 5 * pow(t[i], 2) + 2 * t[i]
            i= i+1
        while t[i]<=2:
            x_tochne[i] = pow(t[i], 4) + 7/3 * pow(t[i], 3) - 12 * pow(t[i], 2) + 19 * t[i] - 8 - 7/3
            y_tochne[i] = 2 * pow(t[i], 4) - pow(t[i], 3) - 22 * pow(t[i], 2) + 51 * t[i] - 23
            i= i+1
        while i<t.size:
            x_tochne[i] = 4/5 * pow(t[i], 5) - 37/12 * pow(t[i], 4) - 17/3 * pow(t[i], 3) + 70 * pow(t[i], 2) - 138 * t[i] - 25/3 * t[i] + 27 - 128/5 +284/3
            y_tochne[i] = 6/5 * pow(t[i], 5) - 5 * pow(t[i], 4) + 25/12 * pow(t[i], 4) - 25 * pow(t[i], 3) + 135 * pow(t[i], 2) - 210 * t[i] - 53/3 * t[i] + 177 - 192/5
            i= i+1
        return t, x, y, x_tochne, y_tochne

    def fi(self, x):
        return x + 2

    def psi(self, x):
        return 2*x

    def f(self, t, x, y, x_zap, x_zap_2, y_zap, y_zap_2):
        return 2*x_zap + y_zap + 2*y_zap_2 + 6*t*t

    def g(self, t, x, y, x_zap, x_zap_2, y_zap, y_zap_2):
        return 4*x_zap + 2*x_zap_2 + y_zap + 2*t

    def draw_save(self, app, t, x, y, x_tochne, y_tochne):
        fig, ax1 = plt.subplots(figsize=(15,5))
        plt.xlabel('x, y, x_tochne, y_tochne')
        plt.ylabel('t')

        plt.plot(t, x)
        plt.plot(t, y)
        plt.plot(t, x_tochne)
        plt.plot(t, y_tochne)

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
        
        
