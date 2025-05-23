import sys                      # 匯入 sys 模組，用來處理應用程式退出
import serial                  # 匯入 pyserial 模組，用於串口通訊
from PyQt5.QtWidgets import (  # 從 PyQt5 匯入建立 GUI 介面所需的元件
    QApplication, QWidget, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox, QLabel
)

# 定義主視窗類別，繼承自 QWidget
class SerialSender(QWidget):
    def __init__(self):
        super().__init__()                     # 呼叫父類別的建構式
        self.setWindowTitle("Serial Sender")   # 設定視窗標題
        self.init_ui()                         # 初始化介面

    def init_ui(self):
        # 建立三個文字輸入框，存入 self.inputs
        self.inputs = [QLineEdit(self) for _ in range(3)]
        
        # 為每個輸入框設定提示文字
        for line_edit in self.inputs:
            line_edit.setPlaceholderText("請輸入一個字元 (如 A)")

        # 建立說明標籤
        self.label = QLabel("請輸入三個字元（例如：A B C）", self)

        # 建立送出按鈕，並連接點擊事件到 send_data 方法
        self.send_button = QPushButton("送出", self)
        self.send_button.clicked.connect(self.send_data)

        # 使用垂直排列的布局方式
        layout = QVBoxLayout()
        layout.addWidget(self.label)  # 加入標籤

        # 加入三個輸入框
        for inp in self.inputs:
            layout.addWidget(inp)

        # 加入送出按鈕
        layout.addWidget(self.send_button)

        # 將此布局設定為視窗的主版面
        self.setLayout(layout)

    # 傳送資料的方法
    def send_data(self):
        # 讀取輸入框文字並去除空白，存入 values
        values = [inp.text().strip() for inp in self.inputs]

        # 檢查是否都有輸入（不得為空）
        if len(values) != 3 or any(len(v) == 0 for v in values):
            QMessageBox.warning(self, "錯誤", "請輸入三個值，例如：A B C")  # 顯示警告
            return  # 結束函式

        try:
            # 開啟指定的串口，鮑率為 9600，timeout 設為 1 秒
            ser = serial.Serial("/dev/ttyAMA5", 9600, timeout=1)

            # 將每個值寫入串口（轉成 UTF-8 並加上換行符號）
            for v in values:
                ser.write(v.encode('utf-8') + b"\n")

            ser.close()  # 傳送完畢後關閉串口

            # 顯示成功訊息
            QMessageBox.information(self, "成功", "資料已傳送")

        except Exception as e:
            # 若開啟串口或傳送過程有錯誤，顯示錯誤訊息
            QMessageBox.critical(self, "錯誤", f"無法開啟串口: {e}")

# 主程式進入點
if __name__ == "__main__":
    app = QApplication(sys.argv)  # 建立應用程式物件
    window = SerialSender()       # 建立主視窗物件
    window.show()                 # 顯示主視窗
    sys.exit(app.exec_())         # 啟動主事件迴圈，結束時正常退出
