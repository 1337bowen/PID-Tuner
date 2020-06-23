
# Instructions:
#  - the user has control over all of the variables exept for the ones labeled simulation values
#  - in the serial plotter, X is the PD controller output, and p is the current angular postion of the system
# Original code in arduino by cheesefacejoe

# Port to Python by Dr. B (2020)

import time
import math
import random
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np

from timeit import default_timer as timer

# PI macro
M_PI = math.pi

# matplotlib vars
x_plot = []
p_plot = []
dt_plot = []

dt = 0.05
ts = np.arange(0, 75, dt)

# simulation speed
d = 40

# Rocket values
mass = 0.846 # in kg
inertia = 0.02 # in kg * m^2
force = 15 # in N
lever = 0.2 # in m

# PD Gains
P = 1
D = 1

# inital angular postion and velocity using degrees
p = 0
v = 2

# constant angular acceleration to simulate something like wind
c = 0

# max and min servo range in degrees
M = 9
m = -(M)

# ammount if noise (0 to 100)
N = 0
n = -(N)

# simulation values
t = 0
X = 0
dR = M_PI / 180
a = 0

start = timer()

for i in range(1, 1000):

  X = (P * -(p)) + (D * -(v))

  if X > M:
    X = M
  
  if X < m:
    X = m
  

  print("X")
  print("\t")
  print(X)
  x_plot.append(X)
  print("\t")

  X = X * dR

  t = lever * force * math.sin(X)

  a = (t / inertia) + c

  v = v + (a * 0.05) + (random.randint(n, N) / 100.0)

  p = p + (v * 0.05) + (random.randint(n, N) / 100.0)
  
  print("p")
  print("\t")
  print(p)
  p_plot.append(p)

  dt_plot.append(timer())

end = timer()
dif = end - start

def c_extend(array):
  array.extend(np.full(len(ts) - len(array), array[0]))

c_extend(p_plot)
c_extend(x_plot)
c_extend(dt_plot)

fig, ax = plt.subplots()

# plt.ylim(-3, 1.5)
plt.ylim(-5, 5)

plt.plot(ts, p_plot, label='P val')
plt.plot(ts, x_plot, label='P val')
plt.plot(ts, dt_plot, label = 'dt')

plt.ylabel("val")
plt.xlabel("ts")

ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

# ax.tick_params(axis='x', colors='white')
# ax.tick_params(axis='y', colors='white')

plt.title('PID Tuner')
plt.show()