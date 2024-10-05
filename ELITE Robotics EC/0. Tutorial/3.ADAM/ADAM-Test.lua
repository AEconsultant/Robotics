--ADAM6051 Test
sleep(1)
--modbus slave IP Address
ip="192.168.1.111"
--modbus slave port
port=502
--get modbus tcp header
ctx=modbus_new_tcp(ip,port)

--connect to modbus header
conState=modbus_connect(ctx)
while (conState==-1) do
	sleep(0.5)
	elite_print("Connection failed")
	conState=modbus_connect(ctx)
end
elite_print("Connection OK")	

function counter(DI_reg_start,DI_reg_end,phase)
	local reg0=DI_reg_start
 	local reg1=DI_reg_end
 	ret0,cnt0=modbus_read_register(ctx,reg0)
 	ret1,cnt1=modbus_read_register(ctx,reg1)
	if (ret0==-1 or ret1==-1) then
        elite_print("Read register error:"..phase)	
    else	
		cnt=math.floor(cnt0+cnt1*(2^16))
	end 
	return cnt
end

i=0
elite_print("Start")
pos0=counter(4009,4010,"A")		
while (i<100) do 
	a=counter(4009,4010,"A")
	set_global_variable("D117",a)
	b=counter(4011,4012,"B")
	set_global_variable("D118",b)
	z=counter(4013,4014,"Z")
	set_global_variable("D119",z)
	
	pos1=counter(4009,4010,"A")
	l_belt=(pos1-pos0)*(200/1000)
	set_global_variable("D120",l_belt)
	
	i=i+1
	sleep(0.1)
end
speed=l_belt/10
elite_print("Conveyor Speed: ",speed)

elite_print("End")
modbus_close(ctx)

