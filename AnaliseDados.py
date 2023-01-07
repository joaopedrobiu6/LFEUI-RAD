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


def Func_to_Fit(par1_, par2_, x):
    y = np.exp(par2_*(x-par1_))
    return y

def Fit(x, y):
    parameters, covariance = curve_fit(Func_to_Fit, x, y, maxfev=2000)

    fit_A = parameters[0]
    fit_B = parameters[1]
    print(fit_A, fit_B)
    fit_y = Func_to_Fit(fit_A, fit_B, x)
    #plot(x, fit_y, "r", "o", "-", "titulo", "xaxis", "yaxis", "savefigura.png")
    return parameters
    
    
def Thresh_Data(i_cap):
    x, y = np.loadtxt('thresh_sweep.txt', dtype=float)
    print(x, y)
    p = Fit(x, y)
    tv1 = np.log(i_cap)/p[1]+p[0]
    tv2 = p[0]
    print('Threshold voltage (I cap method):    ' + str(tv1))
    print('\nThreshold voltage (math method):    ' + str(tv2))


Thresh_Data(0.001)