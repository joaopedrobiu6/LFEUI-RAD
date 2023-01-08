import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def plot(x, y, color_, marker_, linestyle_, title_, xlabel_, ylabel_, filename_):
    x = np.asarray(x)
    y = np.asarray(y)
    p1 = plt.plot(x, y, color=color_, marker=marker_, linestyle=linestyle_)
    p1.title(title_)
    p1.xlabel(xlabel_)
    p1.ylabel(ylabel_) 
    p1.savefig(filename_)
    p1.show()
    return p1, x, y


def Func_to_Fit(x, A, B, C):
    y = A*np.exp(B*(x-C))
    return y

def Fit(x, y, min, max, color1_, color2_, marker_, linestyle_, title_, xlabel_, ylabel_, filename_):
    fig, ax = plt.subplots(1, 1)
    
    parameters, covariance = curve_fit(Func_to_Fit, x, y, maxfev=2000)
    fit_A = parameters[0]
    fit_B = parameters[1]
    fit_C = parameters[2]
    print(f"\npar[0] = {fit_A}\npar[1] = {fit_B}\npar[2] = {fit_C}\n")
    fit_x = np.arange(min, max, 0.05 )
    
    ax.scatter(x, y, marker=marker_, color=color1_)
    ax.plot(fit_x, Func_to_Fit(fit_x, fit_A, fit_B, fit_C), color=color2_, linestyle=linestyle_)
    #ax.annotate([f"par[0] = {fit_A}\n, par[1] = {fit_B},\n fpar[2] = {fit_C}"], (1, 1))

    ax.set_xlabel(xlabel_)
    ax.set_ylabel(ylabel_)
    ax.set_title(title_)
    
    fig.savefig(filename_)
    
    return parameters
    
    
def Thresh_Data(i_cap):
    x, y = np.loadtxt('thresh_sweep.txt', dtype=float)
    print(x, y)
    p = Fit(x, y)
    tv1 = np.log(i_cap)/p[1]+p[0]
    tv2 = p[0]
    print('Threshold voltage (I cap method):    ' + str(tv1))
    print('\nThreshold voltage (math method):    ' + str(tv2))


xdata = [1, 2, 3, 4, 5]
xdata = np.asarray(xdata)
ydata = 2*np.exp(xdata)
ydata = np.asarray(ydata)

Fit(xdata, ydata, 0, 5.1, "red", "orange", "^", "--", "ola", "xx", "yy", "tentativa.png")
