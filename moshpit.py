import pyvisa
import matplotlib.pyplot as plt
import numpy as np 
import scipy as sp
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
                print(Fore.RED+"not getting the reply I expected"+Style.RESET_ALL)
                print("Result is:" + Back.LIGHTRED_EX, res , Style.RESET_ALL)
            break
        time.sleep(0.1)

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


print("COMEÇAR O SWEEP")
print(Fore.LIGHTBLUE_EX + "T inicial: ", time.asctime(), Style.RESET_ALL)


# ESCREVER AQUI O ADRESS DO SMU (VER NO NI-VISA) 
address = 'USB0::0x05E6::0x2636::4083856::INSTR'

res_man = pyvisa.ResourceManager()  # use py-visa backend
  
print(address)
print(res_man.open_resource(address))

try:
    keith = res_man.open_resource(address)
except:
    print('a ligação ao SMU correu mal maninho')
    exit(1)
else:
    keith.write("localnode.prompts=0")
    keith.write("errorqueue.clear()")
    keith.write("*RST")
    keith.write("*CLS")
    time.sleep(.1)

# SE TUDO CORREU BEM ATÉ AQUI PODEMOS ENVIAR O SCRIPT (FALTA METER O NOME NAS '')
load_TSP(keith, 'resist.tsp')
print("escreveu na maquina mpt")

keith.write('SetMeasParam(1, 5, 10, 0.05, 5)')
print("chegou ao geronimo")

waitforcompletion()
#keith.write('*CLS')
npoints=keith.query('print(smub.buffer.getstats(smub.nvbuffer1).n)')
print('Number of points from sweep:', npoints)


#vCurrent = [float(x) for x in keith.query('printbuffer' +'(1, smub.nvbuffer1.n, smub.nvbuffer1.readings)').split(',')]
#vVoltage = [float(x) for x in keith.query('printbuffer' +'(1, smub.nvbuffer1.n, smub.nvbuffer2.readings)').split(',')]

keith.close()
print('closed it')


print('**** data from sweep')
#print(vCurrent)
#print(vVoltage)

exit(0)