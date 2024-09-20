'''
Author: Elite_zhangjunjie
CreateDate: 2021-10-18 17:00:00
LastEditors: Elite_zhangjunjie
LastEditTime: 2021-11-03 17:49:18
Description: RoboDK 监控ELite_EC机器人，在仿真中模拟真实机器人的运动 Monitor the Status of Elite_EC Robot
'''

from robolink.robolink import *    # API to communicate with RoboDK for simulation and offline/online programming
from robodk.robodk import *      # Robotics toolbox for industrial robots
import threading
import socket
import struct
import time


global ROBOT_JOINTS

class EcRobodkDrive:
    
    # define date position ,(start pos,end pos)
    Elite_GET_TIME = 1
    Elite_GET_BUF_LEN = (0,4)
    Elite_GET_JOINT_POSITION = (13,77) 
    Elite_GET_JOINT_SPEEDS = None
    Elite_GET_JOINT_CURRENTS = None
    Elite_GET_TCP_FORCES = None
    
    
    def __init__(self, ip: str = "192.168.1.200", port: int = 8056) -> None:
        self.ip = ip
        self.port = port
    
    
    def __connect(self):
        """create a socket obj connect
        """
        try:
            self.ec_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            # 设置超时时间 set timeout 
            # self.ec_sock.settimeout(8)
            # 连接参数服务器，参数必须为元组格式connect to server
            self.ec_sock.connect((self.ip,self.port))
            # self.ec_sock = socket.create_connection((self.ip,self.port))
            # self.ec_sock.settimeout(8)
        except:
            print("%s连接失败,请检查对应机器人的8056端口是否已经打开connected failed, please confirm the 8056 port" %self.ip)
            quit()
    
    
    def __first_recv(self, buf_len: int = 366):
        """从8056端口中拿取一次数据解析出当前版本对应的数据包长度

        Args:
            buf_len (int, optional): 首次拿取数据的数据包长度. Defaults to 366.
        """
        self.__connect()
        buf_len = buf_len
        first_buf = self.ec_sock.recv(buf_len,socket.MSG_WAITALL)
        self.buf_len = self.get_buf_len(first_buf)
        self.ec_sock.close()
        self.ec_sock = None

    
    def get_buf_len(self,buf: bytes):
        """从字节包中获取长度信息

        Args:
            buf (bytes): 8056返回的字节包

        Returns:
            int: 解析出来的数据包长度
        """
        date_len = buf[self.Elite_GET_BUF_LEN[0]:self.Elite_GET_BUF_LEN[1]]
        if hasattr(self,"buf_len") and self.buf_len[0] != len(buf):
            print("字节长度错误，为the length fault%s" %len(buf))

        print(date_len)
        return struct.unpack("!I",date_len)
    
    
    def get_joint_data(self, buf: bytes):
        """截取关节信息并解析

        Args:
            buf (bytes): 8056返回的字节包

        Returns:
            tuple: 解析出来的关节数据
        """
        joint_byte = buf[self.Elite_GET_JOINT_POSITION[0]:self.Elite_GET_JOINT_POSITION[1]]
        # print(joint_byte)
        return struct.unpack_from("!dddddddd",joint_byte,0)
        
    
    def loop(self):
        """loop process
        """
        self.__first_recv()
        self.__connect()
        
        global ROBOT_JOINTS
        recv_count = 0
        recv_time_last = time.time()
        while True:
            
            buf = self.ec_sock.recv(self.buf_len[0],socket.MSG_WAITALL)

            if self.buf_len != self.get_buf_len(buf):
                print("package length fault，original length%s,atctual length%s" % (self.buf_len,self.get_buf_len(buf)))
                self.ec_sock.close()
                self.__connect()
                continue

            ROBOT_JOINTS = list(self.get_joint_data(buf))
            # print([joint for joint in ROBOT_JOINTS])

            recv_count += 1
            if recv_count % 125 == 0:       #*计算每秒的数据包个数
                t_now = time.time()
                print("Monitoring at %.1f packets per second" % (recv_count/(t_now-recv_time_last)))
                recv_count = 0
                recv_time_last = t_now
                
            # time.sleep(0.008)
            
        self.ec_sock.close()
    
    
# Procedure to check if robot joint positions are different according to a certain tolerance
def Robot_Joints_Check(jA,jB, tolerance_deg=1):
    # 设置一个误差值，从而判断机器人是否真的已经移动啦
    #todo:是否要*pi/180
    if jA is None:
        return True
    
    for i in range(6):
        if abs(jA[i]-jB[i]) > tolerance_deg*pi/180:
            return True
    return False 
    
    
def main_loop():
    """main loop
    """
    global ROBOT_JOINTS

    ROBOT_JOINTS = None
    # init joint data
    last_joints_target = None
    last_joints_refresh = None
    target_count = 0
    
    # Refresh the screen every time the robot position changes
    TOLERANCE_JOINTS_REFRESH   = 0.1
    RETRIEVE_JOINTS_ONCE = False  # If True, the current robot position will be retrieved once only

    # Create targets given a tolerance in degrees
    CREATE_TARGETS = True
    TOLERANCE_JOINTS_NEWTARGET = 10 # in degrees
    
    REFRESH_RATE = 0.1
    
    while 1 :
        
        # 获取线程数量，判断线程是否还在继续运行
        length = len(threading.enumerate())
        if length < 2:
            print("程序退出")
            quit()
        
        # print(ROBOT_JOINTS)
        if ROBOT_JOINTS == None :
            continue
        
        # Set the robot to that position 更新位置
        if Robot_Joints_Check(last_joints_refresh, ROBOT_JOINTS, TOLERANCE_JOINTS_REFRESH):
            last_joints_refresh = ROBOT_JOINTS    
            robot.setJoints(list(ROBOT_JOINTS))
        
        # Stop here if we need only the current position
        if RETRIEVE_JOINTS_ONCE:
            quit(0)
    
        # Check if the robot has moved enough to create a new target
        if CREATE_TARGETS and Robot_Joints_Check(last_joints_target, ROBOT_JOINTS, TOLERANCE_JOINTS_NEWTARGET):
            last_joints_target = ROBOT_JOINTS
            target_count = target_count + 1
            newtarget = RDK.AddTarget('T %i' % target_count, 0, robot)

        # Take a short break        
        pause(REFRESH_RATE)
    

    
    
if __name__ == "__main__":


    # define ec robot ip and port
    ROBOT_IP = None     # default ip : "192.168.1.200"
    
    # create Robodk obj
    RDK = Robolink()

    # get robot obj
    robot = RDK.ItemUserPick("请选择Elite_EC机器人Please select Elite_EC robot", ITEM_TYPE_ROBOT)
    if not robot.Valid():
        quit()
    
    # get robot's ip from robodk frame:
    if ROBOT_IP == None :
        ip,port,path,ftpuser,ftppass = robot.ConnectionParams()
        ROBOT_IP = ip
        
    # create EC robot obj and state loop thread
    ec_robot = EcRobodkDrive(ROBOT_IP)
    threading.Thread(target = ec_robot.loop, daemon = True).start()
    main_loop()

    # threading.Thread(target = main_loop,args=(ROBOT_JOINTS,) , daemon = True).start()
    # ec_robot.loop(ROBOT_JOINTS)