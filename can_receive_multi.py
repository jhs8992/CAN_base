# 디바이스4개 연결했을 때 데이터 받는 방법. 수신만..
# dev1 = motor rpm (ID=100), dev2 = motor voltage(ID=201), dev3 = motor tem(ID=305), dev4 = car yawrate(ID=105)

import can

def motor_rpm(msg):
    rpm = (msg.data[1] << 8 | msg.data[0])
           
def motor_vol(msg):
    vol = msg.data[0]

def motor_tem(msg):
    tem = msg.data[0]

def car_yawrate(msg):
    yaw = msg.data[0]

bus = can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=500000)

try:
    while True:
        msg = bus.recv(timeout = 1.0)

        if msg is None:
            continue

        if msg.arbitration_id == 0x100:
            motor_rpm(msg)

        elif msg.arbitration_id == 0x201:
            motor_vol(msg)

        elif msg.arbitration_id == 0x305:
            motor_tem(msg)

        elif msg.arbitration_id == 0x105:
            car_yawrate(msg)
except KeyboardInterrupt:
    a= 1
finally:
    bus.shutdown()

