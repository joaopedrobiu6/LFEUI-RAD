import pyvisa
import numpy as np
import matplotlib.pyplot as plt
import time
from colorama import Fore, Back, Style

"""
SMU A - GATE
SMU B - DRAIN

waitforcompletion() - mete o programa em espera até o SMU acabar as suas tarefas

load_TSP() - envia o script .tsp para o SMU

reset() - reset smua e smub

sweepA() - curva de threshold voltage; varia a Tensão (v) na Gate (SMU A) e obtém a Corrente (i) na Drain (SMU B)

sweepB() - tensão de saturação; varia a Tensão (v) na Drain (SMU B) e obtém a Corrente (i) na Drain (SMU B)

"""


def waitforcompletion():
    pos = 0

    while 1:
        try:
            res = keith.query("*OPC?")
        except:
            print("\r", " " * pos, ":-(", "", end="")
            res2 = keith.read()
            pos += 1
        else:
            # print('read opc=',res)
            if res.find("1") == 0:
                print("\r", " :-) " * pos)
            else:
                print("not getting the reply I expected")
                print("Result is:", res)
            break
        time.sleep(0.3)


def load_TSP(inst, script):
    """Load an anonymous TSP script into the K2636 nonvolatile memory."""
    try:
        # loads and runs the script and this defines the functions
        inst.write("loadandrunscript")
        line_count = 1
        for line in open(script, mode="r"):
            # print(line)
            inst.write(line)
            line_count += 1
        inst.write("endscript")
        print("----------------------------------------")
        print("Uploaded TSP script: ", script, " with {} lines".format(line_count))

    except FileNotFoundError:
        print("ERROR: Could not find tsp script. Check path.")
        raise SystemExit


def reset(inst):
    inst.write("smua.reset()")
    inst.write("smub.reset()")


def sweepA(inst, inf, sup, nstep):  # CHANGE VGS MEASURE IDS - THRESHOLD VOLTAGE
    current = []
    voltage = []
    step = float((sup - inf) / nstep)

    for i in range(0, nstep, 1):
        vbias = inf + i * step
        temp_volt = "smua.source.levelv=" + f"{vbias}"
        inst.write(temp_volt)
        waitforcompletion()
        inst.write("smub.measure.i(smub.nvbuffer1)")
        inst.write("smua.measure.v(smua.nvbuffer1)")
        waitforcompletion()
        a = float(
            inst.query("printbuffer(1, smub.nvbuffer1.n, smub.nvbuffer1.readings)")
        )
        waitforcompletion()
        current.append(a)
        b = float(
            inst.query("printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)")
        )
        waitforcompletion()
        voltage.append(b)

    reset(inst)
    return voltage, current


def sweepB(inst, inf, sup, nstep):  # CHANGE VDS MEASURE IDS   -  SATURATION VOLTAGE
    current = []
    voltage = []
    step = float((sup - inf) / nstep)

    for i in range(0, nstep, 1):
        vbias = inf + i * step
        temp_volt = "smub.source.levelv=" + f"{vbias}"
        inst.write(temp_volt)
        waitforcompletion()
        inst.write("smub.measure.i(smub.nvbuffer1)")
        inst.write("smub.measure.v(smub.nvbuffer2)")
        waitforcompletion()
        a = float(
            inst.query("printbuffer(1, smub.nvbuffer1.n, smub.nvbuffer1.readings)")
        )
        waitforcompletion()
        current.append(a)
        b = float(
            inst.query("printbuffer(1, smub.nvbuffer2.n, smub.nvbuffer2.readings)")
        )
        waitforcompletion()
        voltage.append(b)

    reset(inst)
    return voltage, current


#######################################################################################
#######################################################################################
###################################### PROGRAMA #######################################
#######################################################################################
#######################################################################################

address = "USB0::0x05E6::0x2636::4083856::INSTR"  # endereço da máquina

res_man = pyvisa.ResourceManager()  # use py-visa backend

try:
    keith = res_man.open_resource(address)
except:
    print("a ligação ao SMU correu mal maninho")
    exit(1)
else:
    keith.write("localnode.prompts=0")
    keith.write("errorqueue.clear()")
    keith.write("*RST")
    keith.write("*CLS")
    time.sleep(0.1)

# SE TUDO CORREU BEM ATÉ AQUI PODEMOS ENVIAR O SCRIPT (FALTA METER O NOME NAS '')
load_TSP(keith, "config.tsp")
print("meteu o script la dentro")

#################################################################################################
#################################################################################################
########################################### Standalone Measures #################################
#################################################################################################
#################################################################################################

data = open("data.txt", "w")

# ZERO GATE
# MEDIR A CORRENTE NA DRAIN COM A VOLTAGEM NA GATE A ZERO
keith.write("setup_ZeroGateV()")
waitforcompletion()
a = float(keith.query("printbuffer(1, smub.nvbuffer1.n, smub.nvbuffer1.readings)"))
waitforcompletion()
reset(keith)
print("Zero Gate:    ")
print(a)
data.write("Zero Gate:    " + str(a))

# Gate Body Leak
# MEDIR A CORRENTE NA GATE COM A VOLTAGEM NA DRAIN A ZERO
keith.write("setup_GBLeak()")
waitforcompletion()
b = float(keith.query("printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)"))
waitforcompletion()
reset(keith)
print("\nGate Body Leakage, Forward:    ")
print(b)
data.write("\nGate Body Leakage, Forward:    " + str(b))

# resistencia saturacao
# IMPOR UMA CORRENTE NA DRAIN E UMA VOLTAGEM NA GATE E MEDIR A RESISTENCIA NA DRAIN
keith.write("setup_ResistDS()")
waitforcompletion()
c = float(keith.query("printbuffer(1, smub.nvbuffer1.n, smub.nvbuffer1.readings)"))
waitforcompletion()
reset(keith)
print("\nDS Resistance:    ")
print(c)
data.write("\nDS Resistance:    " + str(c))

# corrente saturaçao
# IMPOR UMA VOLTAGEM NA DRAIN E NA GATE E MEDIR CORRENTE NA DRAIN
keith.write("setup_OnStateD()")
waitforcompletion()
d = float(keith.query("printbuffer(1, smub.nvbuffer1.n, smub.nvbuffer1.readings)"))
waitforcompletion()
reset(keith)
print("\nDS current(sat):    ")
print(d)
data.write("\nDS current(sat):    " + str(d))

data.close()

#######################################################################################
#######################################################################################
####################################### SWEEPS ########################################
#######################################################################################
#######################################################################################

#### THRESHOLD VOLTAGE SWEEP ####
# Curva de threshold voltage; varia a Tensão (v) na Gate (SMU A) e obtém a Corrente (i) na Drain (SMU B)
keith.write("setup_tresh(10)")
a, b = sweepA(keith, 0.1, 3, 30)
print(a, b)

plt.plot(a, b, "-r")
plt.savefig("thresh_sweep_graph.png")
plt.clf()
np.savetxt("thresh_sweep.txt", [a, b])


#### SATURATION VOLTAGE SWEEP ####
# Tensão de saturação; varia a Tensão (v) na Drain (SMU B) e obtém a Corrente (i) na Drain (SMU B)
keith.write("setup_satv()")
c, d = sweepB(keith, 0, 5, 30)
print(c, d)
plt.plot(c, d, "-b")
plt.savefig("satv_sweep_graph.png")
np.savetxt("satv_sweep.txt", [c, d])
