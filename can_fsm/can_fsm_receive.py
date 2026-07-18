import can
import can_random_data 

class CAN_FSM:
    def __init__(self, frame_data):
        #self.frame_data = bin(frame_data)[2:].zfill(16)
        self.frame_data = frame_data
        self.dlc_byte = int(frame_data[15:19],2)
        self.max_data_bit = 19 + self.dlc_byte*8
        self.max_crc_bit = self.max_data_bit + 16
        self.max_ack_bit = self.max_crc_bit + 2

        self.state = "receive_check"

        self.state_func = {
            "receive_check" : self.func_receive_check,
            "sof" : self.func_sof,
            "arbitration" : self.func_arbitration, 
            "rtr" : self.func_rtr,
            "reserved" : self.func_reserved,
            "dlc" : self.func_dlc,
            "data" : self.func_data,
            "crc" : self.func_crc,
            "ack" : self.func_ack,
            "eof" : self.func_eof,
        }

    def run(self):
        while True:
            func = self.state_func.get(self.state)
            if func:
                func()
            if self.state == "DONE":
                break

    def func_receive_check(self):
        data_frame = self.frame_data
        if data_frame:
            print("데이터 정상으로 받음")
            self.state = "sof"
        else:
            print(" NO FRAME DATA ")
            self.state = "DONE"

    def func_sof(self):
        sof_bit = self.frame_data[0]
        #print(self.frame_data)
        #print(sof_bit)
        if sof_bit == '0':
            print("SOF비트 확인 완료")
            self.state = 'arbitration'
        else:
            print(sof_bit)
            print("SOF비트 확인 불가")
            self.state = "DONE"

    def func_arbitration(self):
        id_bit = self.frame_data[1:12]
        #id_bit_hex = hex(int(id_bit,2))
        print("CAN ID: ",id_bit)
        #print("ID:",id_bit_hex)
        self.state = "rtr"

    def func_rtr(self):
        rtr_bit = self.frame_data[12]
        if rtr_bit == '0':
            print("rtr 비트 확인 결과 데이터에 정보 존재함")
            self.state = "reserved"
            #self.state = "DONE"
        elif rtr_bit == '1':
            print("rtr 비트 확인 결과 데이터 필요로 함")
            self.state = "DONE"

    def func_reserved(self):
        reserved_bit = self.frame_data[13:15]
        print("reserved bits: ",reserved_bit)
        self.state = "dlc"
    
    def func_dlc(self):
        dlc_bit = self.frame_data[15:19]
        dlc_byte = int(dlc_bit,2)
        print("dlc: ",dlc_bit)
        print("dlc_byte(데이터 바이트): ",dlc_byte)
        self.state = "data"


    def func_data(self):
        #max_data_bit = (19 + self.dlc_byte*8)
        f_data = self.frame_data[19:self.max_data_bit]
        hex_data = hex(int(f_data,2))
        #print(self.max_data_bit)
        print("데이터 길이: ", len(f_data))
        print("데이터 값: ",hex_data)
        self.state = "crc"

    def func_crc(self):
        crc_bit = self.frame_data[self.max_data_bit:self.max_crc_bit]
        print("crc: ",crc_bit)
        self.state = "ack"
        
    def func_ack(self):
        ack_bit = self.frame_data[self.max_crc_bit:self.max_ack_bit]

        if ack_bit == '11':
            print("ack(데이터 수신 이상 무): ",ack_bit)
            self.state = "eof"

        else:
            self.state = "DONE"

    def func_eof(self):
        eof_bit = self.frame_data[self.max_ack_bit:]
        #print(len(eof_bit))
        print("데이터 수신 완료")
        print("eof: ",eof_bit)

        self.state = "DONE"

if __name__ == "__main__":
    data = can_random_data.random_data()
    print("------------------------------------")
    fsm_receive = CAN_FSM(frame_data = data) 
    fsm_receive.run() 