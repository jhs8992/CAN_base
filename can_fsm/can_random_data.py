import random

def random_data():
    random_dlc = random.randint(1,8)
    max_num = 2**(random_dlc*8)-1  
    random_number = random.randint(1, max_num) 
    bit_size = random_number.bit_length() 
    #byte_size = (bit_size + 7) // 8 

    sof = [0] 
    arbitration_bits = [1,1,0,0,1,0,0,1,0,0,0] 

    rtr = [0] 
    reserved = [0,0] 
    dlc = [int(bit) for bit in f"{random_dlc:04b}"] 
    data = [int(bit) for bit in f"{random_number:0{random_dlc*8}b}"] 
    crc = [1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0] 
    ack = [1,1] 
    eof = [1,1,1,1,1,1,1] 

    can_frame_bit = sof + arbitration_bits + rtr + reserved + dlc + data + crc + ack + eof 
    bit_string = "".join(str(bit) for bit in can_frame_bit)
    can_frame_bit_size = len(can_frame_bit) 
    
    
    print("랜덤수:",random_number)
    print("랜덤수 바이트:",random_dlc)
    print("dlc 배열:",dlc)
    print("프레임 비트 수:",can_frame_bit_size)
    #print("프레임 비트:",can_frame_bit)
    

    #return can_frame_bit
    return bit_string