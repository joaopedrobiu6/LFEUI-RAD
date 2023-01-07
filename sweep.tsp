--[[


-- set parameters 

function SetMeasParam(startV, stopV, step, idrain)
    if not (startV and stopV and step and idrain) then print ('ERRO')
        return
    end 
    reset()


    -- config SMU

    smua.source.func = smua.OUTPUT_DCAMPS 
    display.smua.measure.func = display.MEASURE_OHMS   ?
    smua.source.leveli = idrain
    smua.nvbuffer1.clear()    ?

    smub.source.func = smub.OUTPUT_DCVOLTS 
    display.smub.measure.func = display.MEASURE_DCVOLTS 
    smub.source.levelv = startV
    smub.nvbuffer1.clear()


    --sweeppppp
    Output()
    for vbias = startV, stopV, step do 
        smub.source.levelv = vbias
        smub.measure.v(smub.nvbuffer1)    ?
        smua.measure.r(smua.nvbuffer1)     ?
    end
    Output()
    return 
end


-- para nao termos de estar sempre a trocar o output

function Output()
    if smua.source.output = 1 then 
        smua.source.output = 0 
        smub.source.output = 0
    else 
        smua.source.output = 1
        smub.source.output = 1
    end
end

--]]



-- Ok vou tentar algo que perceba 

function SetMeasParam(startV, stopV, step, vdrain)
    if not (startV and stopV and step and idrain) then print ('ERRO')
        return
    end 
    reset()


    -- config SMU

    smua.source.func = smua.OUTPUT_DCVOLTS 
    -- display.smua.measure.func = display.MEASURE_DCAMPS   
    smua.source.levelv = startV
    smua.nvbuffer1.clear()

    smub.source.func = smub.OUTPUT_DCVOLTS 
    display.smub.measure.func = display.MEASURE_DCAMPS 
    smub.source.levelv = vdrain
    smub.nvbuffer1.clear()


    --sweeppppp
    
    smua.source.output = smua.OUTPUT_ON
    smub.source.output = smub.OUTPUT_ON
    i=0
    for vbias = startV, stopV, step do 
        smua.source.levelv = vbias
        smub.measure.i(smub.nvbuffer1)  
          i++ 
        
           
    end
    
    return 
end

------------------------------
function MeasAmps(vbias, vdrain)
    --fixar os limites
    smua.source.func = smua.OUTPUT_DCVOLTS 
    display.smua.measure.func = display.MEASURE_DCAMPS   
    smua.nvbuffer1.clear()

    smub.source.func = smub.OUTPUT_DCVOLTS 
    display.smub.measure.func = display.MEASURE_DCAMPS 
    smub.source.levelv = vdrain
    smub.nvbuffer1.clear()

    
    smua.source.output = smua.OUTPUT_ON
    smub.source.output = smub.OUTPUT_ON

    smua.source.levelv = vbias
    smub.measure.i(smub.nvbuffer1)  
