import numpy 
import matplotlib.pyplot as plt

def graficos(x, y):
    plt.plot(x, y, '-r')
    plt.xlabel("eixo x")
    plt.ylabel("eixo y")
    plt.title("titulo")
    plt.savefig("plot.png")

ax = [0.1, 0.2, 0.3, 0.4]
ay = [1, 2, 3, 4]

graficos(ax, ay)