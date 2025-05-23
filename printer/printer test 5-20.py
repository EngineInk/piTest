import serial
import time

# 使用 /dev/ttyAMA5
ser = serial.Serial(
    port="/dev/ttyAMA5",
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)

def esc(cmd):  # ESC/POS 指令封裝
    return bytes(cmd)

# 初始化印表機
ser.write(esc([0x1B, 0x40]))  # 初始化 ESC @
time.sleep(0.1)

# Name 行 + 底線（模擬方式）
ser.write(b"Name: Steven\n")
ser.write(esc([0x1B, 0x2D, 0x01]))  # 開底線
ser.write(b"             ^\n")      # 用符號模擬底線
ser.write(esc([0x1B, 0x2D, 0x00]))  # 關底線

# Gender 行（加粗）
ser.write(esc([0x1B, 0x45, 0x01]))  # 開加粗
ser.write(b"Gender - male\n")
ser.write(esc([0x1B, 0x45, 0x00]))  # 關加粗

# IP 資訊
ser.write(b"Computer IP: 10.0.0.166\n")

# 分隔線
ser.write(b"-" * 40 + b"\n")

# Record 訊息
ser.write(b"Record: {Steven speak:}\"Hello Wo\n")
ser.write(b"rld! \"\n")

# 換行與切紙（視印表機支援）
ser.write(b"\n\n")
ser.write(esc([0x1D, 0x56, 0x00]))  # 切紙 ESC/POS 全切

# 關閉串列埠
ser.close()
