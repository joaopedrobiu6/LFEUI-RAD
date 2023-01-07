function setup_tresh(vdrain)
    smua.reset()
    smub.reset()

    smua.source.func=smua.OUTPUT_DCVOLTS 
    display.smua.measure.func=display.MEASURE_DCVOLTS
    --smub.source.limiti=0.2  
    smua.nvbuffer1.clear()
    smub.source.func=smub.OUTPUT_DCVOLTS 
    display.smub.measure.func=display.MEASURE_DCAMPS 
    smub.source.levelv=vdrain
    smub.nvbuffer1.clear()

    
    smua.source.output = smua.OUTPUT_ON
    smub.source.output = smub.OUTPUT_ON
end  

function setup_GraficoBonito()
    smua.reset()
    smub.reset()
    
    smua.source.func=smua.OUTPUT_DCVOLTS 
    display.smua.measure.func=display.MEASURE_DCVOLTS
    smub.source.limiti=0.2  
    smua.nvbuffer1.clear()
    smub.source.func=smub.OUTPUT_DCVOLTS 
    display.smub.measure.func=display.MEASURE_DCAMPS 
    smua.source.levelv=-2
    smub.nvbuffer1.clear()
    smua.nvbuffer2.clear()
    smub.nvbuffer2.clear()


    
    smua.source.output = smua.OUTPUT_ON
    smub.source.output = smub.OUTPUT_ON
end  

function setup_ZeroGateV()
    smua.reset()
    smub.reset()
    
    smua.source.func=smua.OUTPUT_DCVOLTS 
    smub.source.func=smub.OUTPUT_DCVOLTS
    display.smub.measure.func=display.MEASURE_DCAMPS
    --smub.source.limiti=0.2  
    smua.nvbuffer1.clear()
    smub.nvbuffer1.clear()

    smub.source.levelv=-40
    smua.source.levelv=0
   
    smua.source.output = smua.OUTPUT_ON
    smub.source.output = smub.OUTPUT_ON

    smub.measure.i(smub.nvbuffer1)
end  

function setup_GBLeak()
    smua.reset()
    smub.reset()
    
    smua.source.func=smua.OUTPUT_DCVOLTS 
    smub.source.func=smub.OUTPUT_DCVOLTS
    display.smua.measure.func=display.MEASURE_DCAMPS
    --smua.source.limiti=0.2  
    smua.nvbuffer1.clear()
    smub.nvbuffer1.clear()

    smub.source.levelv=0
    smua.source.levelv=-20
   
    smua.source.output = smua.OUTPUT_ON
    smub.source.output = smub.OUTPUT_ON

    smua.measure.i(smua.nvbuffer1)
end  


function setup_ResistDS()
    smua.reset()
    smub.reset()
    
    smua.source.func=smua.OUTPUT_DCVOLTS 
    smub.source.func=smub.OUTPUT_DCAMPS
    display.smub.measure.func=display.MEASURE_OHMS 
    smua.nvbuffer1.clear()
    smub.nvbuffer1.clear()

    smub.source.leveli=-0.05
    smua.source.levelv=-4.5
   
    smua.source.output = smua.OUTPUT_ON
    smub.source.output = smub.OUTPUT_ON

    smub.measure.r(smub.nvbuffer1)
end

function setup_OnStateD()
    smua.reset()
    smub.reset()
    
    smua.source.func=smua.OUTPUT_DCVOLTS 
    smub.source.func=smub.OUTPUT_DCVOLTS
    display.smub.measure.func=display.MEASURE_DCAMPS

    smua.nvbuffer1.clear()
    smub.nvbuffer1.clear()


    smub.source.levelv=-25
    smua.source.levelv=-10
   
    smua.source.output = smua.OUTPUT_ON
    smub.source.output = smub.OUTPUT_ON

    smub.measure.i(smub.nvbuffer1)
end

function setup_Tconduct()
    smua.reset()
    smub.reset()
   
    smua.source.func=smua.OUTPUT_DCVOLTS 
    display.smua.measure.func=display.MEASURE_DCVOLTS
    smub.source.func=smub.OUTPUT_DCVOLTS 
    display.smub.measure.func=display.MEASURE_DCAMPS 

    smub.source.levelv=vdrain

    smub.nvbuffer1.clear()
    smua.nvbuffer1.clear()

    --smub.source.limiti=0.2 

    smua.source.output = smua.OUTPUT_ON
    smub.source.output = smub.OUTPUT_ON

    --smua.source.levelv = vbias
    --smub.measure.i(smub.nvbuffer1)
end