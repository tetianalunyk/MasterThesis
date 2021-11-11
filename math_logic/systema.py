import numpy as np
import parser
import os, shutil
import uuid
import matplotlib.pyplot as plt
import math
from flask import *


class Systema:
    def __init__(self, step, tau_1, tau_2, alpha, beta, gama, func_1="", func_2="", func_3=""): # formula is optional
        self.step = step
        self.tau_1 = tau_1
        self.tau_2 = tau_2
        self.alpha = alpha
        self.beta = beta
        self.gama = gama
        self.func_1 = func_1
        self.func_2 = func_2
        self.func_3 = func_3


    def calculate(self):
        T=35
        t = np.arange(0, 35 + 2*self.step, self.step)
        x = np.zeros(t.size)
        y = np.zeros(t.size)
        z = np.zeros(t.size)
        v = np.zeros(t.size)
        u = np.zeros(t.size)
        l = np.zeros(t.size)
        p = np.zeros(t.size)
        q = np.zeros(t.size)
        d = np.zeros(t.size)
        x[0] = self.fi(0)
        y[0] = self.psi(0)
        z[0] = self.ksi(0)
        i = 1
        while t[i-1]-self.tau_1 < 0 and t[i-1] <= T:
                v[i-1] = self.fi(t[i-1]-self.tau_1)
                u[i-1] = self.psi(t[i-1]-self.tau_1)
                x[i] = x[i-1] + self.step * self.S(t[i-1], x[i-1], y[i-1], z[i-1], self.fi(t[i-1]-self.tau_1), self.fi(t[i-1]-self.tau_2), self.psi(t[i-1]-self.tau_1), self.psi(t[i-1]-self.tau_2), self.ksi(t[i-1]-self.tau_1), self.ksi(t[i-1]-self.tau_2))
                y[i] = y[i-1] + self.step * self.I(t[i-1], x[i-1], y[i-1], z[i-1], self.fi(t[i-1]-self.tau_1), self.fi(t[i-1]-self.tau_2), self.psi(t[i-1]-self.tau_1), self.psi(t[i-1]-self.tau_2), self.ksi(t[i-1]-self.tau_1), self.ksi(t[i-1]-self.tau_2))
                z[i] = z[i-1] + self.step * self.R(t[i-1], x[i-1], y[i-1], z[i-1], self.fi(t[i-1]-self.tau_1), self.fi(t[i-1]-self.tau_2), self.psi(t[i-1]-self.tau_1), self.psi(t[i-1]-self.tau_2), self.ksi(t[i-1]-self.tau_1), self.ksi(t[i-1]-self.tau_2))
                i = i+1

        while t[i-1]-self.tau_2 < 0 and t[i-1]<=T:
                k = np.searchsorted(t, t[i-1]-self.tau_1)
                v[i-1] = (t[i-1]-self.tau_1-t[k]) / self.step * x[k+1] + (t[k+1]- t[i-1]+self.tau_1) / self.step * x[k]
                u[i-1] = (t[i-1]-self.tau_1-t[k]) / self.step * y[k+1] + (t[k+1]- t[i-1]+self.tau_1) / self.step * y[k]
                l[i-1] = (t[i-1]-self.tau_1-t[k]) / self.step * z[k+1] + (t[k+1]- t[i-1]+self.tau_1) / self.step * z[k]
                x[i] = x[i-1] + self.step * self.S(t[i-1], x[i-1], y[i-1], z[i-1], v[i-1], self.fi(t[i-1]-self.tau_2), u[i-1], self.psi(t[i-1]-self.tau_2), l[i-1], self.ksi(t[i-1]-self.tau_2))
                y[i] = y[i-1] + self.step * self.I(t[i-1], x[i-1], y[i-1], z[i-1], v[i-1], self.fi(t[i-1]-self.tau_2), u[i-1], self.psi(t[i-1]-self.tau_2), l[i-1], self.ksi(t[i-1]-self.tau_2))
                z[i] = z[i-1] + self.step * self.R(t[i-1], x[i-1], y[i-1], z[i-1], v[i-1], self.fi(t[i-1]-self.tau_2), u[i-1], self.psi(t[i-1]-self.tau_2), l[i-1], self.ksi(t[i-1]-self.tau_2))
                i = i+1

        while t[i-1]<T:
                k = np.searchsorted(t, t[i-1]-self.tau_1)
                m = np.searchsorted(t, t[i-1]-self.tau_2)
                v[i-1] = (t[i-1]-self.tau_1-t[k]) / self.step * x[k+1] + (t[k+1]- t[i-1]+self.tau_1) / self.step * x[k]
                u[i-1] = (t[i-1]-self.tau_1-t[k]) / self.step * y[k+1] + (t[k+1]- t[i-1]+self.tau_1) / self.step * y[k]
                l[i-1] = (t[i-1]-self.tau_1-t[k]) / self.step * z[k+1] + (t[k+1]- t[i-1]+self.tau_1) / self.step * z[k]
                p[i-1] = (t[i-1]-self.tau_2-t[m]) / self.step * x[m+1] + (t[m+1]- t[i-1]+self.tau_2) / self.step * x[m]
                q[i-1] = (t[i-1]-self.tau_2-t[m]) / self.step * y[m+1] + (t[m+1]- t[i-1]+self.tau_2) / self.step * y[m]
                d[i-1] = (t[i-1]-self.tau_2-t[m]) / self.step * z[m+1] + (t[m+1]- t[i-1]+self.tau_2) / self.step * z[m]
                x[i] = x[i-1] + self.step * self.S(t[i-1], x[i-1], y[i-1], z[i-1], v[i-1], p[i-1], u[i-1], q[i-1], l[i-1], d[i-1])
                y[i] = y[i-1] + self.step * self.I(t[i-1], x[i-1], y[i-1], z[i-1], v[i-1], p[i-1], u[i-1], q[i-1], l[i-1], d[i-1])
                z[i] = z[i-1] + self.step * self.R(t[i-1], x[i-1], y[i-1], z[i-1], v[i-1], p[i-1], u[i-1], q[i-1], l[i-1], d[i-1])
                i = i+1

        return t, x, y, z

    def fi(self, _x):
        code = parser.expr(self.func_1).compile()
        x = _x
        return eval(code)

    def psi(self, _x):
        code = parser.expr(self.func_2).compile()
        x = _x
        return eval(code)

    def ksi(self, _x):
        code = parser.expr(self.func_3).compile()
        x = _x
        return eval(code)

    def S(self, t, s, i, r, s_zap_1, s_zap_2, i_zap_1, i_zap_2, r_zap_1, r_zap_2):
        return -self.beta*s_zap_1*i_zap_1

    def I(self, t, s, i, r, s_zap_1, s_zap_2, i_zap_1, i_zap_2, r_zap_1, r_zap_2):
        return self.beta*s_zap_1*i_zap_1 - self.gama*i_zap_2 - self.alpha*i

    def R(self, t, s, i, r, s_zap_1, s_zap_2, i_zap_1, i_zap_2, r_zap_1, r_zap_2):
        return self.gama*i_zap_2

    def draw_save(self, app, t, x, y, z):
        fig, ax1 = plt.subplots(figsize=(15,5))
        plt.xlabel('x, y, z')
        plt.ylabel('t')

        plt.plot(t, x)
        plt.plot(t, y)
        plt.plot(t, z)

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
        
        
