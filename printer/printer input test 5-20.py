import serial

# 開啟串口（範例以 ttyAMA5 為例）
ser = serial.Serial("/dev/ttyAMA5", 9600, timeout=1)

# 輸入
Input = input("Input (e.g., A B C): ")
InputDataForPrint = Input.strip().split()

if len(InputDataForPrint) != 3:
    print("請輸入三個值，例如：A B C")
    exit()

# 一個一個印出來
for i in range(3):
    ser.write(InputDataForPrint[i].encode('utf-8') + b"\n")

ser.close()
