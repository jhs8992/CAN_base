import random
import can

class CAN_FSM:
    def __init__(self, can_id):
        self.can_id = can_id
        self.state = "IDLE"
        
        #can 하드웨어 초기화
        '''    
        try:
            self.bus = can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=500000)
        except can.CanError:
            exit()
        '''
       
        self.state_func = {
            "IDLE": self.func_idle,
            "ARBITRATION": self.func_arbitration,
            "TRANSMIT": self.func_transmit,
            "ACK": self.func_ack,
            "ERROR": self.func_error 
        }    

    def run(self):
        while True:
            func = self.state_func.get(self.state)
            if func:
                func()
            if self.state == "DONE":
                break

    def func_idle(self):
        #버스 선로 확인 코드
        bus_path = 1 #버스 선로 clear
        #bus_path = 0 #버스 선로 clear X
        if bus_path:
            self.state = "ARBITRATION"

    def func_arbitration(self):
        #우선순위 확인 코드
        possible = 1
        if possible:
            self.state = "TRANSMIT"
        else:
            self.state = "IDLE"

    def func_transmit(self):
        max_num = 2**64-1 
        random_number = random.randint(1, max_num) 
        bit_size = random_number.bit_length() 
        byte_size = (bit_size + 7) // 8 
        sof = [0] 
        arbitration_bits = [1,1,0,0,1,0,0,1,0,0,0]
        rtr = [0] 
        reserved = [0,0] 
        dlc = [int(bit) for bit in f"{byte_size:04b}"]
        data = [int(bit) for bit in f"{random_number:064b}"]
        crc = [1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0] 
        ack = [1,1] #2bit
        eof = [1,1,1,1,1,1,1] 
        can_frame_bit = sof + arbitration_bits + rtr + reserved + dlc + data + crc + ack + eof 

        can_frame_bit_size = len(can_frame_bit)
        print("프레임 비트 수:",can_frame_bit_size)

        # 실제로는 데이터를 이렇게 보냄
        # self.bus.send(can_frame_bit) 

        self.state = "ACK"

    def func_ack(self):
        #ack 신호를 확인하여 오류가 있었는지 확인
        ack_state = 1 # 정상 전송 완료
        #ack_state = 0 # 비정상 전송
        if ack_state:
            self.state = "DONE"
        else:
            self.state = "ERROR"

    def func_error(self):
        print("전송 과정에서 오류 발생")
        self.state = "IDLE"


if __name__ == "__main__":
    fsm_test = CAN_FSM(can_id=0x201) #변수에 클래스 할당
    fsm_test.run() #클래스 안의 함수 실행
