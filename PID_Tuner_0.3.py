# Original code in arduino by cheesefacejoe

# Port to Python by Dr. B (2020)

# Updates in Python by cheesefacejoe and Dr. B

# remove all print statements for a faster simulation

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np
import math
import random

# simulation speed in s
s = 0.05

# simulation length in s
d = 15

# Rocket values
mass = 0.4 # in kg
inertia = 0.02 # in kg * m^2
force = 12 # in N
lever = 0.4 # in m

# PID Gains
P = 1
I = 0.02
D = 1

# inital angular postion and velocity using degrees
p = 4
v = 10

# constant angular acceleration to simulate something like wind or poor TVC allignment
c = 3

# max and min servo range in degrees
M = 9
m = -M

# ammount of noise (0 to 100)
N = 9
n = -N

# simulation values
t = 0
X = 0
i = 0
dR = math.pi / 180
a = 0
count = 0
xPrev = 0

# matplotlib vars
ts = np.arange(0, d, s)
x_plot = []
p_plot = []
v_plot = []
a_plot = []

print(math.pi / 180)

print("Simulating")

while(count < d):
    i -= p

    xPrev = X

    X = (P * -p) + (I * i) + (D * -v)

    if X > M:
        X = M
  
    if X < m:
        X = m

    print("PID value")
    print(X)

    x_plot.append(X)

    X *= dR
    
    xPrev *= dR
    
    t = lever * force * np.sin((X + xPrev) / 1.9) # (X + xPrev) / 1.9 is here to approximate the rate that the servo turns

    a = (t / inertia) + c

    v = v + (a * s) + (random.randint(n, N) / 100.0)

    p = p + (v * s) + (random.randint(n, N) / 100.0)
    
    # uncomment all of the lines from here to the end of the program for extra information
    
    #print("Angular Acceleration")
    #print(a)
    #print("Angular Velocity")
    #print(v)
    #a_plot.append(a)
    #v_plot.append(v)
    
    print("Angular Position")
    print(p)
    p_plot.append(p)

    count += s

print("Finished")

def c_extend(array):
  array.extend(np.full(len(ts) - len(array), array[0]))

c_extend(x_plot)
c_extend(p_plot)
#c_extend(a_plot)
#c_extend(v_plot)

fig, ax = plt.subplots()

plt.ylim(-12, 12)
plt.plot(ts, x_plot, label = 'PID Output')
plt.plot(ts, p_plot, label = 'Angular Position')

#plt.plot(ts, a_plot, label = 'Angular Acceleration')
#plt.plot(ts, v_plot, label = 'Angular Velocity')

plt.ylabel("Angle (D)")
plt.xlabel("Time (S)")
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
plt.title('PID Tuner')
plt.legend()
plt.show()
