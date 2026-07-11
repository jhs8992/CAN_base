#PCAN모듈을 연결했을 때의 수신 코드 -> 재미나이가 PCAN이 유명하다고 해서 이걸로 해봄
import can

try:
    bus = can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=500000)
except can.CanError:
    exit()

try: 
    while True:
       msg = bus.recv(timeout=1.0)

       if msg is not None:
           if msg.arbitration_id == 0x201:
            receive_data = (msg.data[1]*256)+msg.data[0]
           
       else:
           print("응 데이터 없어")


except KeyboardInterrupt:
    print("수신 끝")

finally:
    bus.shutdown()