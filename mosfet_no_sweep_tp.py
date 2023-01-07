import pyvisa
import numpy as np  
import matplotlib.pyplot as plt 
import time
from colorama import Fore, Back, Style

def waitforcompletion():
    pos = 0

    while 1 :
        try:
            res=keith.query('*OPC?')
        except:
            print('\r',' '*pos,':-(','',end='')
            pos+=1
        else:
            if res.find('1')==0:
                print('\r',' :-) '*pos)
            else:
                print("not getting the reply I expected")
                print("Result is:", res)
            break
        time.sleep(0.5)

def load_TSP(inst, script):
    """Load an anonymous TSP script into the K2636 nonvolatile memory."""
    try:
        # loads and runs the script and this defines the functions
        inst.write('loadandrunscript')
        line_count = 1
        for line in open(script, mode='r'):
            #print(line)
            inst.write(line)
            line_count += 1
        inst.write('endscript')
        print('----------------------------------------')
        print('Uploaded TSP script: ', script,
              ' with {} lines'.format(line_count))

    except FileNotFoundError:
        print('ERROR: Could not find tsp script. Check path.')
        raise SystemExit

def reset(inst):
        
    inst.write('smua.source.levelv=0')
    inst.write('smub.source.levelv=0')
    inst.write('smua.source.output = smua.OUTPUT_OFF')
    inst.write('smub.source.output = smub.OUTPUT_OFF')


address = 'USB0::0x05E6::0x2636::4083856::INSTR'

res_man = pyvisa.ResourceManager()  

try:
    keith = res_man.open_resource(address)
except:
    print('a ligacao ao SMU correu mal maninho')
    exit(1)
else:
    keith.write("localnode.prompts=0")
    keith.write("errorqueue.clear()")
    keith.write("*RST")
    keith.write("*CLS")
    time.sleep(.1)


load_TSP(keith, 'configTP2104.tsp')
print("meteu o script la dentro")

#ZERO GATE 
keith.write('setup_ZeroGateV()')
waitforcompletion()
a = float(keith.query('printbuffer(1, smub.nvbuffer1.n, smub.nvbuffer1.readings)'))
reset(keith)
print('Zero Gate:    ')
print(a)
waitforcompletion()

#Gate Body Leak
keith.write('setup_GBLeak()')
waitforcompletion()
b = float(keith.query('printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)'))
reset(keith)
print('\nGate Body Leakage, Forward:    ')
print(b)
waitforcompletion()

#resistencia saturacao
keith.write('setup_ResistDS()')
waitforcompletion()
c = float(keith.query('printbuffer(1, smub.nvbuffer1.n, smub.nvbuffer1.readings)'))
reset(keith)
print('\nDS Resistance:    ')
print(c)
waitforcompletion()

#corrente saturaçao
keith.write('setup_OnStateD()')
waitforcompletion()
d = float(keith.query('printbuffer(1, smub.nvbuffer1.n, smub.nvbuffer1.readings)'))
reset(keith)
print('\nDS current(sat):    ')
print(d)


waitforcompletion()

np.savetxt('values_tp.txt', np.c_[a, b,c,d])