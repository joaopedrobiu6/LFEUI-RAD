import pyvisa
import numpy as np
import matplotlib.pyplot as plt
import time
from colorama import Fore, Back, Style


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
        time.sleep(0.5)


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


def sweepA(inst, inf, sup, nstep):
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
        voltage.append(
            float(
                inst.query("printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)")
            )
        )
        # a = inst.query('printbuffer(1, smub.nvbuffer1.n, smub.nvbuffer1.readings)')
        # v.append(float(a))
        # print(inst.query(''))
    # print(inst.query('printbuffer(1, smub.nvbuffer1.n, smub.nvbuffer1.readings)'))
    # print(inst.query('printbuffer(1, smub.nvbuffer1.n, smub.nvbuffer1.readings)').length)

    inst.write("smua.source.levelv=0")
    inst.write("smub.source.levelv=0")
    inst.write("smua.source.output = smua.OUTPUT_OFF")
    inst.write("smub.source.output = smub.OUTPUT_OFF")
    # v = [float(x) for x in inst.query('printbuffer' +'(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)').split(',')]
    # inst.write('smua.source.levelv=0.5')
    return voltage, current


def sweepB(inst, inf, sup, nstep):
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
        # a = inst.query('printbuffer(1, smub.nvbuffer1.n, smub.nvbuffer1.readings)')
        # v.append(float(a))
        # print(inst.query(''))
    # print(inst.query('printbuffer(1, smub.nvbuffer1.n, smub.nvbuffer1.readings)'))
    # print(inst.query('printbuffer(1, smub.nvbuffer1.n, smub.nvbuffer1.readings)').length)

    inst.write("smua.source.levelv=0")
    inst.write("smub.source.levelv=0")
    inst.write("smua.source.output = smua.OUTPUT_OFF")
    inst.write("smub.source.output = smub.OUTPUT_OFF")
    # v = [float(x) for x in inst.query('printbuffer' +'(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)').split(',')]
    # inst.write('smua.source.levelv=0.5')
    return voltage, current


address = "USB0::0x05E6::0x2636::4083856::INSTR"

res_man = pyvisa.ResourceManager()  # use py-visa backend

# print(address)
# print(res_man.open_resource(address))

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
load_TSP(keith, "configTP2104.tsp")
print("meteu o script la dentro")

keith.write("setup_tresh(-10)")
print("correu a funçao do setup")
a, b = sweepA(keith, -2.6, -0.1, 30)
print(a, b)


plt.plot(a, b, "-r")
plt.savefig("sweep_tp.png")
plt.clf()
np.savetxt("thresh_sweep_tp.txt", np.c_[a, b])


# printbuffer(1, smub.nvbuffer1.n, smub.nvbuffer1.readings)

# v = [float(x) for x in keith.query('printbuffer' +'(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)').split(',')]
# print(v)
keith.write("setup_GraficoBonito()")
print("correu a funçao do setup")
c, d = sweepB(keith, -5, 0, 30)
print(c, d)
plt.plot(c, d, "-b")
plt.savefig("sweep2_tp.png")
np.savetxt("satv_sweep_tp.txt", np.c_[c, d])
# waitforcompletion()
