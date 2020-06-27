# Original code in arduino by cheesefacejoe

# Port to Python by Dr. B (2020)

# Updates in Python by cheesefacejoe and Dr. B

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np
import math
import random

# simulation length in s (keep as a whole number and do not go above 8)
d = 8

# Rocket values
mass = 0.5 # wet mass + dry mass / 2 in kg
inertia = 0.015 # in kg * m^2
force = 15 # in N
lever = 0.5 # in m

# PID Gains
P = 1
I = 0
D = 0

# inital angular postion and velocity using degrees
p = 1
av = 0

#mount offset to account for poor TVC allignment
offset = 0

# angular acceleration range to simulate wind
c = random.randint(10, 50) / 10.0
randMult = random.randint(-3, 3)

# max and min servo range in degrees
M = 9
m = -M

# ammount of noise (0 to 100)
N = 0
n = -N

# simulation values
t = 0 # torque
X = 0 # PID output
i = 0 # integral
dR = math.pi / 180 # degrees to radians
aa = 0 # angular acceleration
count = 0 # simulation progression
s = 0.04 # simulation refresh rate in s
pPrev = p
avPrev = av

# matplotlib stuff
ts = np.arange(0, d, s)
x_plot = []
p_plot = []
av_plot = []
aa_plot = []
f_plot = []
z_plot = []

print("Simulating")

while(count < d):
    i -= p # calculate the integral

    X = (P * -pPrev) + (I * i) + (D * -avPrev) + offset # PID calculations using one cycle old values
    
    # keeps the PID output in a range to account for min/max TVC angle 
    if X > M + offset:
        X = M + offset
  
    if X < m - offset:
        X = m - offset

    x_plot.append(X - offset)

    pPrev = p
    avPrev = av
   
    t = lever * force * np.sin(X * dR) # calculate the torque applied to the vehicle by the engine

    aa = (t / inertia) + randMult * (np.sin(c * count) + np.sin(math.pi * count)) # calcualte the angular acceleration caused by the torque and by wind

    av = av + (aa * s) + (random.randint(n, N) / 100.0) # calculate angular velocity and add noise

    p = p + (av * s) + (random.randint(n, N) / 100.0) # calculate angular position and add noise
    
    p_plot.append(p)
    z_plot.append(0)

    count += s

print("Finished")

def c_extend(array):
  array.extend(np.full(len(ts) - len(array), array[0]))

c_extend(x_plot)
c_extend(p_plot)
c_extend(z_plot)

fig, ax = plt.subplots()

plt.ylim(-15, 15)
plt.plot(ts, x_plot, label = 'PID Output')
plt.plot(ts, p_plot, label = 'Angular Position')
plt.plot(ts, z_plot, color = 'black')

plt.ylabel("Angle (D)")
plt.xlabel("Time (S)")
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
plt.title('PID Tuner')
plt.legend()
plt.show()
