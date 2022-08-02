#CASE NO. 3
#Input is 4 people at the middle of the 2D grid

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation

print("2D diffusion equation solver")

ppl_length = 10
max_iter_time = 100

D = 2     #Diffusivity

delta_x = 1 #delta_x = delta_y = 1

delta_t = (delta_x ** 2)/(4 * D)   #condition for numerical stability
gamma = (D * delta_t) / (delta_x ** 2)

# Initialize solution: the grid of u(k, i, j) k = time, i = y, j = x
u = np.empty((max_iter_time, ppl_length, ppl_length))

# Initial condition everywhere inside the grid
u_initial = 0

# Boundary conditions
u_max = 100.0
u_min = 0.0

# Set the initial condition
u.fill(u_initial)
u[:, 5, 5] = 100.0

# Set the boundary conditions
u[:, 4:6, 4:6] = u_max
# u[:, (ppl_length-1):ppl_length, 1] = u_left
# u[:, 0:1, 8:9] = u_bottom
# u[:, 8:9, (ppl_length-1):] = u_right


ppl_hist = []  #list to keep track of number of people above a threshold of information density

def calculate(u, threshold):
    for k in range(0, max_iter_time-1, 1):
        for i in range(1, ppl_length-1, delta_x):
            for j in range(1, ppl_length-1, delta_x):
                u[k + 1, i, j] = gamma * (u[k][i+1][j] + u[k][i-1][j] + u[k][i][j+1] + u[k][i][j-1] - 4*u[k][i][j]) + u[k][i][j]
        h = sum(1 for i in u[k, :, :].flatten() if i>= threshold)
        ppl_hist.append(h)
        u[:, 4:6, 4:6] = 100.0

    return u

def plotdensitymap(u_k, k):
    # Clear the current plot figure
    plt.clf()

    plt.title(f"Case 4: Information density map at t = {k} iterations")
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
anim.save('/home/shashank/Shashank Hiremath/Sem 5 content/Transport phenomena/My CFA Stuff/Images/case4.gif', writer='imagemagick', fps=100)

plt.show()

plt.figure()
plt.plot(ppl_hist)
plt.title("The diffusion of information in Case 4")
plt.xlabel("Iterations")
plt.ylabel("No. of people above threshold")
plt.show()

#Histogram to understand variation in information density values
data = u[max_iter_time-1].flatten()
bins_list = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
plt.hist(data, bins_list)
plt.title("Histogram of I(x,y, maximum iteration) in Case 4")
plt.xlabel("I(x,y) value")
plt.ylabel("No. of people")
plt.show()

print("Done!")
