sleep(1)
--modbus slave IP Address
ip="10.3.6.122"
--modbus slave port
port=502
--get modbus tcp header
ctx=modbus_new_tcp(ip,port)

-- Output Bits
robotIsOn=530
workIsDone=531

-- Input Bits
workIsReady=532

--connect to modbus header
conState=modbus_connect(ctx)
while (conState==-1) do
	sleep(0.05)
	elite_print("Connection failed")
	conState=modbus_connect(ctx)
end
elite_print("Connection OK")	


while true do

	------------------------------------------------
	------ Send data from M virtual variables ------
	------------------------------------------------	

	-- get variable state of the output bits 
	retMrobotIsOn = get_robot_io_status("M"..tostring(robotIsOn))
	retMworkIsDone = get_robot_io_status("M"..tostring(workIsDone))
	
	-- set an output array
	value_array = {retMrobotIsOn,retMworkIsDone}
	
	-- write the values to the equivalent robot M variables 
	ret=modbus_write_bits(ctx ,robotIsOn,#value_array , value_array)

	---------------------------------------------
	------ Get data from M virtual variables ----
	---------------------------------------------

	-- Reads intended input M variable from slave
	ret1 = modbus_read_bits(ctx , workIsReady, 1)

	--check for error
	if(ret1==-1)then       
		elite_print("Read error")
	end

	--set local M variable with slave robot M value
	set_robot_io_status("M"..tostring(workIsReady) , ret1[1] // 1)

	sleep(0.1)
end

elite_print("End")
modbus_close(ctx)