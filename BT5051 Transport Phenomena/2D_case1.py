#CASE NO. 1
#Input is 4 adjacent people at the top of the 2D grid

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation

print("2D diffusion equation solver")

ppl_length = 10
max_iter_time = 150

D = 2     #Diffusivity

delta_x = 1 #delta_x = delta_y = 1

delta_t = (delta_x ** 2)/(4 * D)   #condition for numerical stability
gamma = (D * delta_t) / (delta_x ** 2)

# Initialize solution: the grid of u(k, i, j) k = time, i = x, j = y
u = np.empty((max_iter_time, ppl_length, ppl_length))

# Initial condition everywhere inside the grid
u_initial = 0

u_max = 100.0
u_min = 0.0

# Set the initial condition
u.fill(u_initial)

# Set the boundary conditions
u[:, (ppl_length-1):, 3:8] = u_max
u[:, :, :1] = u_min
u[:, :1, 1:] = u_min
u[:, :, (ppl_length-1):] = u_min

ppl_hist = []  #list to keep track of number of people above a threshold of information density

def calculate(u, threshold):
    for k in range(0, max_iter_time-1, 1):
        for i in range(1, ppl_length-1, delta_x):
            for j in range(1, ppl_length-1, delta_x):
                u[k + 1, i, j] = gamma * (u[k][i+1][j] + u[k][i-1][j] + u[k][i][j+1] + u[k][i][j-1] - 4*u[k][i][j]) + u[k][i][j]
        h = sum(1 for i in u[k, :, :].flatten() if i>= threshold)
        ppl_hist.append(h)

    return u

def plotdensitymap(u_k, k):
    # Clear the current plot figure
    plt.clf()

    plt.title(f"Case 1: Information map at t = {k} iterations")
    plt.xlabel("x")
    plt.ylabel("y")

    # This is to plot u_k (u at time-step k)
    plt.pcolormesh(u_k, cmap='jet', vmin=0, vmax=100)
    plt.colorbar()

    return plt

# Do the calculation here with a set threshold value
u = calculate(u, 20)

def animate(k):
    plotdensitymap(u[k], k)

anim = animation.FuncAnimation(plt.figure(), animate, interval=1, frames=max_iter_time, repeat=False)
anim.save('/home/shashank/Shashank Hiremath/Sem 5 content/Transport phenomena/My CFA Stuff/Images/case1.gif', writer='imagemagick', fps=100)

plt.show()

plt.figure()
plt.plot(ppl_hist)
plt.title("The diffusion of information in Case 1")
plt.xlabel("Iterations")
plt.ylabel("No. of people above threshold")
plt.show()

#Histogram to understand variation in information density values
data = u[max_iter_time-1].flatten()
bins_list = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
plt.hist(data, bins_list)
plt.title("Histogram of I(x,y, maximum iteration) in Case 1")
plt.xlabel("I(x,y) value")
plt.ylabel("No. of people")
plt.show()

print("Done!")
