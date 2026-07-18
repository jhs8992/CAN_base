#can프레임 구현 코드
#SOF, arbitration bits, RTR, Reserved, DLC, DATA, CRC-15, ACK, EOF 
import random
random_dlc = random.randint(1,8)
max_num = 2**(random_dlc*8)-1 
#max_num = 2**64-1 # 64비트일 때 max 숫자
random_number = random.randint(1, max_num) 
bit_size = random_number.bit_length() # 비트 크기
#byte_size = (bit_size + 7) // 8 # 비트 사이즈



sof = [0] #1bit
arbitration_bits = [1,1,0,0,1,0,0,1,0,0,0] #201 할 생각임 b 1100 1001 000 = 201

###########################################################################################################
# 궁금증 있음: arbitration_bit를 리틀엔디안 때문에 반전시킨 후 can_frame_bit에 합쳐야 하는지, 아님 그냥 합치는지#
###########################################################################################################

rtr = [0] #1bit
reserved = [0,0] #2bit
dlc = [int(bit) for bit in f"{random_dlc:04b}"] # 랜덤 숫자 바이트 크기를 이진수로 변환
data = [int(bit) for bit in f"{random_number:0{random_dlc*8}b}"] # 랜덤 숫자 이진수 변환 
crc = [1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0] #16 bit
ack = [1,1] #2bit
eof = [1,1,1,1,1,1,1] #7bit

can_frame_bit = sof + arbitration_bits + rtr + reserved + dlc + data + crc + ack + eof #전체 프레임 비트

can_frame_bit_size = len(can_frame_bit) #비트 크기

print("랜덤수:",random_number)
print("랜덤수 바이트:",random_dlc)
print("dlc 배열:",dlc)
print("프레임 비트 수:",can_frame_bit_size)
print("프레임 비트:",can_frame_bit)