function SetMeasParam(start, stop, num, limitI, nplc)

    -- config SMU

    smub.reset()
    smub.source.func =      smub.OUTPUT_DCVOLTS 
    smub.source.limiti =    limitI
    smub.measure.nplc =     nplc                     --o q 
    smub.measure.delay =     smub.DELAY_AUTO          --o q 


    -- prepare Buffers
    smub.nvbuffer1.clear()
	smub.nvbuffer2.clear()

    -- displays
    display.smub.measure.func = display.MEASURE_DCAMPS
    display.screen = display.SMUB                   -- o q 

    --Config Trigger
    smub.trigger.source.linearv(start, stop, num)
    smub.trigger.source.limiti      = limitI
    smub.trigger.measure.action     = smub.ENABLE       -- faz medies
    smub.trigger.measure.iv(smub.nvbuffer1, smub.nvbuffer2)
    smub.trigger.endpulse.action    = smub.SOURCE_HOLD  -- nao volta ao valor zero entre os pontos, tipo escadinha
    smub.trigger.endsweep.action    = smub.SOURCE_IDLE  -- volta ao zero no final
    smub.trigger.count              = num
    smub.trigger.source.action      = smub.ENABLE       -- faz o sweep
    smub.measure.autozero           = smub.AUTOZERO_ONCE -- caga
    smub.measure.delay              = -1                -- auto
    --smub.measure.lowrangi = 10e-3


   

    -- Begin test
    beeper.beep(1, 400)
    smub.source.output = smub.OUTPUT_ON
    smub.trigger.initiate()
    waitcomplete()
    smub.source.output = smub.OUTPUT_OFF

    -- Print data
    for x=1, smub.nvbuffer1.n do
        print(smub.nvbuffer2[x], smub.nvbuffer1[x])
    end

    print("smub.nvbuffer1.n",smub.nvbuffer1.n)

    
    return 
end