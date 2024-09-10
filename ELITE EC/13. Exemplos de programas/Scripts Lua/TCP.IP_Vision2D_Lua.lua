while(1) do 

	D5 = get_global_variable("D5")

	if (D5 ~= 0) then 
		elite_print("D5:",D5)
		server_ip = "192.168.1.20"
		server_port = "22"
		-- Connect to TCP server with specified IP and port
		a = connect_tcp_server(server_ip,server_port) 
		elite_print("connect_tcp_server return ",tostring(a)) 
		
		while(D5 ~= 0) do 
			-- The client sends data "T" to the server
			client_send_data(server_ip,"T") 
			sleep(1) 
			
			-- Receive data from the server 
			ret,recv = client_recv_data(server_ip) 
			elite_print("data from server length =",ret,"data=",recv)
			
			if (ret >= 1) then 
				-- Return the substring after removing the first and last characters
				-- Ex: "[300,200,0,0]"
				str1 = string.sub(recv,2,-2)
				elite_print("sub", str1) 
				
				-- Use "," to separate strings
				str2 = str1:split(",") 
				x = str2[1] 
				y = str2[2] 
				rz = str2[3] 
				result = str2[4]
				
				set_global_variable("D1",x) 
				set_global_variable("D2",y) 
				set_global_variable("D3",rz) 
				set_global_variable("D0",result) 
				set_global_variable("D5",0) 
				D5 = 0 
			end 
			D5 = 0 
		end 
	else 
		sleep(0.5) 
	end
end

