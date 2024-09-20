-- ==============================================================================
-- ELITE ROBOT – Robótica Industrial Equinotec
-- Av. Villagarcia de Arosa, 1120
-- 4450-300 Matosinhos
-- T. +351 229 350 755 / T. +351 218 400 850 
-- Email: info@eliterobots.pt
-- 01/2024
-- ==============================================================================
-- 								ELITE - LUA COMMANDS  
-- ==============================================================================

-- ########## VARIABLES ##########

// ===== READ: B/I/D/P/V =====
A = get_global_variable ("B001")
B = get_global_variable ("I001")
C = get_global_variable ("D001")
A,B,C,D,E,F = get_global_variable ("P001")
A,B,C,D,E,F = get_global_variable ("V001")
elite_print("P1 J1:",A,"J2:",B,"J3:",C,"J4:",D,"J5:",E,"J6:",F)

// ===== WRITE: B/I/D/P/V =====
set_global_variable ("B001", 5)
set_global_variable ("I001", 5)
set_global_variable ("D001", 5)
set_global_variable ("P001",1,1,1,1,1,1)
set_global_variable ("V001",1,1,1,1,1,1)



-- ########## I/Os ##########

// ===== READ: X/Y/M =====
A = get_robot_io_status("I1") 		-- X001 
A = get_robot_io_status("O1")		-- Y001 
A = get_robot_io_status("M1")		-- M001
A = get_robot_io_status("M400")		-- M400 
A = get_robot_io_status("AI1")      -- AI001 

// ===== WRITE: Y/M =====
set_robot_io_status("O1",1)			-- Y001 
set_robot_io_status("M528",1)		-- M528 
set_robot_io_status("AO1",11.123)	-- AO001



-- ########## CONTROL ##########

-- Branch Statement
if (exp1) then
	--[execute the statement block when exp1 is true]
elseif (exp2) then
	--[execute the statement block when exp2 is true]
else
	--[execute the statement block when other conditions are met]
end

-- While Loop
while (exp) do
	--[exp loop the statement block when the expression is true]
	sleep(0.001)
end

-- Repeat Loop
repeat
	--[loop the statement block when the expression is false]
until (exp)

-- For Loop
for init, max/min value, increment do
	--[execute statement block]
end

-- Function Definition Syntax
function MyFunc (param1, param2)
	--[do something]
return param1, (param1+param2)
end

-- Function Call 
x,y = MyFunc (a, b)

-- Label 
::start::
goto start



-- ########## MANAGING STRING DATA ##########

-- Returns the substring after removing the first and last characters
str1 = string.sub(recv,2,-2)
-- Use "," to separate strings
str2 = str1:split(",")
-- Assignment
x = str2[1] 
y = str2[2]
-- length of string
str = string.len(s)
-- convert uppercase letters in lowercase
str = string.lower(s)
-- convert lowercase letters in uppercase
str = string.upper(s)
-- convert character to number
str=string.char(s)
-- convert number to character 
str=string.byte(s)



-- ########## ROBOT STATUS MONITORING ##########

-- Acquire Robot Mode (0-TEACH mode, 1-PLAY mode, 2-REMOTE mode)
A = get_robot_mode()
-- Acquire JBI File Running Mode (0-Step, 1-Cycle, 2-Continous)
A = get_cycle_mode()
-- Acquire Servo Status (0-servo disabled, 1-servo enabled)
A = get_servo_status()
-- Acquire Robot State (0-Stopped, 1-Paused, 3-Running, 4-Alarmed)
A = get_robot_state()
-- Acquire Robot Current Frame (0-JOINT, 1-WLD(Cartesian), 2-TOOL, 3-USER, 4-CYL(Cylindrical))
A = get_current_coord()
-- Acquire Robot Cartesian Position ([x,y,z,rx,ry,rz], (x,y,z in mm, rx,ry,rz in radians))
A = get_robot_pose()
String = string.format("%s,%s,%s,%s,%s,%s",tostring(A[1]),tostring(A[2]),tostring(A[3]),tostring(A[4]),tostring(A[5]),tostring(A[6])) 
elite_print("string: ", String)
-- Acquire Robot Joint Pose ([J1,J2,J3,J4,J5,J6,0,0] (in degree))
A = get_robot_joint()
-- Acquire Robot Torque ([torque1,torque2,torque3,torque4,torque5,torque6,0,0])
A = get_robot_torque()
-- Acquire Tool Coordinates System
A = get_tool_frame(3)
-- Acquire User Coordinates System
A = get_user_frame(5)
-- Check whether the specified tool is enabled (1-Enabled, 0-Disabled)
A = check_tool_frame_enable(0)
-- Check whether the specified user is enabled (1-Enabled, 0-Disabled)
A = check_user_frame_enable(4)
-- Get register interface of M variable (index: byte definition, range: 0-190)
get_robot_register (77)
-- Set the register interface of the M variable (index: byte definition, size: The unit is byte, string: hex string
set_robot_register (66,2,"0000")
-- Get register interface of M variable (192-477)
get_robot_extra_register (192)
-- Set the register interface of the M variable (192-477)
set_robot_extra_register (192,4,"00000000")
-- Get current tcp speed
get_current_tcp_spd ()

-- Commands applicable to V2.17.0 and above.
-- Get the current tool coordinate system number
A = get_tool_no ()
-- Get the current user coordinate system number
A = get_user_no ()
-- Get the pose data of the Flange center in the current base coordinate system
get_flange_pose_inbase ()
-- Get the pose of the Flange center in the current user coordinate system
get_flange_pose_inUser ()
-- Get the pose of the current TCP in the current user coordinate system
get_tcp_pose_inuser ()
-- Get the robot pose ([x,y,z,rx,ry,rz], (x,y,z in mm, rx,ry,rz in radians))
get_tcp_pose ()
-- Get end 485 mode (0-initial mode, 1-tci communication mode, 2-modbusRTU master station mode)
get_terminal_485_mode ()


-- ########## OTHERS ##########

-- Delay
sleep (double second);	

-- Debug info: 0 - do not output information, 1 - output information
set_debug(1)

-- Print
elite_print("X000:",tostring(A))

-- Cinemática
pose = {378.538,212.504,134.055,-2.712,-0.791,2.553}
joint = {10.081,-75.007,105.449,-70.694,98.434,89.481,0.000,0.000}

-- Transform Cartesian pose -> Joint pose
	-- (the reference point needs to be close to the target point)
Inv_data = get_inv_kinematics(pose, joint)

-- Transform Joint pose -> Cartesian pose
Fwd_data = get_fwd_kinematics(joint)

-- Inverse of Position: Transform Cartesian position to Joint pose ????
pose_inv_data=pose_inv({0,1,2,3,4,5})

--  Pose Multiplication ????
pose_mul_data=pose_mul(var1, var2)

-- Declarations
String = "abcdef"
Array  = {1,2,3.0}

-- Get system timestamp (s)
A = os.time()
	
	
-- ########## COMMUNICATION - TCP/IP ##########

// ===== TCP Client =====
-- ===== Connection to the server =====
server_ip = "192.168.1.100"
server_port = "22"
-- A==1.0: connected / A==0.0: failed  
A = connect_tcp_server(server_ip,server_port)
elite_print("connect_tcp_server return ",tostring(A))
	-- Alternative
	connect_tcp_server("192.168.1.100",22)
sleep (1)

-- ===== Receive data from the server =====
-- ret==-1.0: no data / ret>=1: data length (Ex: "11")
-- recv==(vazio): no message / recv== message (Ex:"[300,0,0,0]") 
ret,recv = client_recv_data(server_ip,2) 
elite_print("data (from server) length =",ret,"data=",recv)
	-- Alternative (with timout)
	ret,recv = client_recv_data(server_ip,0.1)

-- ===== Send data to the server =====
-- Send data "T" (string) to the server
snd = client_send_data(server_ip,"T") 
if (snd == -1) then 
	elite_print("error send server")
end

-- ===== Disconnection from server =====
disconnect_tcp_server(server_ip)


// ===== TCP Server =====
--The port connected to client
port = 6666
--The IP Address of client
ip = "192.168.1.100"
--initialize TCP server
init_tcp_server (port)
sleep (5)

while(1)do
	--decide if client is connected to server
	ret= is_client_connected (ip)
	if (ret == 1)then
		--server send msg to client
		server_send_data (ip ,"1")
		recv="1"
		while(recv ~= "2") do
			sleep (1)
			--Server receive data from client
			Ret,recv= server_recv_data (ip)
			elite_print("data length=",ret,"data=",recv)
		end
	end
end



-- ########## COMMUNICATION - RS485 -> CONTROLLER ##########

-- ===== Open the terminal 485 interface ===== 
-- ret==-1.0:error / ret>=0:open succeeded 
ret = rs485_open()

-- ===== Configure RS485 interface ===== 
-- ret==-1.0:error / ret>=0:open succeeded 
-- rs485_setopt(int speed, int bits, string event, int stop) 
config = rs485_setopt(9600,8,"N",1)

-- ===== Receive data from RS485 interface =====
-- ret<=0: no data / ret>=1: data length
-- recv==(empty): no message / recv== message
-- rs485_recv(int timeout, int hex) int hex=1-> hexadecimal message 
--int hex=0->other 
ret,recv = rs485_recv(100,0)

-- ===== Send data to RS485 interface =====
-- rs485_send(string buff, int hex) int hex=1-> hexadecimal message
--int hex=0->other
snd = rs485_send("buff",0)

-- ===== Close RS485 interface =====
-- ret==-1.0:error / ret>=0:close succeeded
ret = rs485_close()



-- ########## COMMUNICATION - RS485 -> TOOL END ##########

-- ===== Open the terminal 485 interface ===== 
-- ret==-1.0:error / ret>=0:open succeeded 
ret = tci_open() 

-- ===== Configure serial port of RS485 interface -> flange ===== 
-- ret==-1.0:error / ret>=0:open succeeded 
-- tci_setopt(int speed, int bits, string event, int stop) 
config = tci_setopt(9600,8,"N",1)

-- ===== Receive data from RS485 interface -> flange =====
-- ret<=0: no data / ret>=1: data length
-- recv==(empty): no message / recv== message
-- tci_recv(int timeout, int hex) int hex=1-> hexadecimal message 
-- int hex=0->other 
ret,recv = tci_recv(100,0)

-- ===== Send data to RS485 interface -> flange =====
-- tci_send(string buff, int hex) int hex=1-> hexadecimal message
-- int hex=0->other
snd = tci_send("buff",0) 

-- ===== Close RS485 interface -> flange =====
-- ret==-1 :error / ret>=0 :close succeeded
ret = tci_close()



-- ########## COMMUNICATION - MODBUS MASTER - TCP/RTU ##########
sleep(5)
-- Acquire Modbus TCP handle
-- Modbus_new_tcp(char* ip,int port)
ctx = modbus_new_tcp ("192.168.1.100",6666)
-- Acquire Modbus RTU handle
-- Modbus_new_rtu(int choose,int baud,char parity,int data_bit,int stop_bit)
ctx = modbus_new_rtu (0,9600,78,8,1)

-- Open Modbus Handle
modbus_connect (ctx) 

-- Set slave address
ret1 = modbus_set_slave(ctx,0x3)
if(ret1==-1)then
	elite_print("Wrong address")
end  

-- Write values to Register
ret2 = modbus_write_register(ctx,771,1)        
if(ret2==-1)then     
	elite_print("Write error")
end

-- Writes value to the specified Coil
-- int modbus_write_bit(ctx,int reg,int value)
modbus_write_bit(ctx,1,1)

-- Write values to multiple Coils
-- int modbus_write_bits(ctx,int reg,int size,table value)
value_array = {1,1,1}
modbus_write_bits(ctx,1,3,value_array)

-- Read the signal value from the specified Register
-- int,int Modbus_read_register (ctx,int reg)
ret3,value = modbus_read_register(ctx,771)        
if(ret3==-1)then       
	elite_print("Read error")
end
elite_print("value is:",value)

-- Read the signal value from the specified Coil
-- table modbus_read_bits(ctx,int reg,int len)
ret4 = modbus_read_bit(ctx,771,1)

-- Close Modbus Handle
modbus_close (ctx)

