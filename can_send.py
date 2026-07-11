#PCAN모듈을 연결했을 때의 송신 코드 -> 재미나이가 PCAN이 유명하다고 해서 이걸로 해봄
import can
import time

try:
    bus = can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=500000)
except can.CanError:
    exit()
try: 
    while True:
        msg = can.message(arbitration_id = 0x201, 
                          data=[0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
                          is_extended_id = False)
        bus.send(msg)
        time.sleep(1)

except KeyboardInterrupt:
    print("송신 끝")

finally:
    bus.shutdown()