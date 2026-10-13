import numpy as np
from scipy import signal

# Parametros globales

fs = 1000            # frecuencia de muestreo [Hz]
dt = 1 / fs          # paso de tiempo [s]
f0 = 2               # frecuencia de las señales periódicas [Hz]
T0 = 1 / f0          # periodo [s]
A  = 1               # amplitud

# Eje de tiempo de las entradas periodicas: 

t_x = np.arange(0, 2, dt)

#1) Señales periodicas

def senoidal(t):   return A * np.sin(2*np.pi*f0*t)
def cuadrada(t):   return A * signal.square(2*np.pi*f0*t)
def triangular(t): return A * signal.sawtooth(2*np.pi*f0*t, width=0.5)
def diente(t):     return A * signal.sawtooth(2*np.pi*f0*t, width=1)
 
periodicas = {
    "Senoidal": senoidal(t_x),
    "Cuadrada": cuadrada(t_x),
    "Triangular": triangular(t_x),
    "Diente de sierra": diente(t_x),
}

#2) Señales aperiodicas (respuestas a impulso)
#Eje de tiempo de las h(t): -1 a 3 s

t_h = np.arange(-1, 3, dt)
 
def u(t):
    return (t >= 0).astype(float)
 
def exp_decreciente(t): return np.exp(-t) * (u(t) - u(t-1))
def exp_creciente(t):   return np.exp(t)  * (u(t) - u(t-1))
def impulso(t):
    d = np.zeros_like(t)
    d[np.argmin(np.abs(t))] = 1/dt   # área = 1  →  aproxima δ(t)
    return d
def escalon(t):         return u(t)
def sinc(t):            return np.sinc(t/np.pi)   # = sin(t)/t
 
aperiodicas = {
    "Exp. decreciente": exp_decreciente(t_h),
    "Exp. creciente": exp_creciente(t_h),
    "Impulso": impulso(t_h),
    "Escalón": escalon(t_h),
    "Sinc": sinc(t_h),
}