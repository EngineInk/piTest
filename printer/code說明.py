import serial  # 匯入 pyserial 模組，用來進行串口通訊

# 開啟串口，這裡以 /dev/ttyAMA5 為例（適用於 Raspberry Pi 或 Linux 系統），
# 設定鮑率為 9600，timeout 為 1 秒
ser = serial.Serial("/dev/ttyAMA5", 9600, timeout=1)

# 從使用者輸入一行資料，例如：A B C
Input = input("Input (e.g., A B C): ")

# 去除前後空白，並以空格分隔成清單，例如輸入 "A B C" 會變成 ["A", "B", "C"]
InputDataForPrint = Input.strip().split()

# 檢查是否正好輸入三個值，若不是則提示錯誤並結束程式
if len(InputDataForPrint) != 3:
    print("請輸入三個值，例如：A B C")
    exit()

# 將每個輸入的值一個一個寫入串口，每個後面都加上換行符號
for i in range(3):
    ser.write(InputDataForPrint[i].encode('utf-8') + b"\n")

# 傳送完畢後關閉串口
ser.close()
