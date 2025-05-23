import sys
import serial
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox, QLabel
)

class SerialSender(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Serial Sender")
        self.init_ui()

    def init_ui(self):
        self.inputs = [QLineEdit(self) for _ in range(3)]
        for line_edit in self.inputs:
            line_edit.setPlaceholderText("請輸入一個字元 (如 A)")

        self.label = QLabel("請輸入三個字元（例如：A B C）", self)

        self.send_button = QPushButton("送出", self)
        self.send_button.clicked.connect(self.send_data)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        for inp in self.inputs:
            layout.addWidget(inp)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

    def send_data(self):
        values = [inp.text().strip() for inp in self.inputs]
        if len(values) != 3 or any(len(v) == 0 for v in values):
            QMessageBox.warning(self, "錯誤", "請輸入三個值，例如：A B C")
            return

        try:
            ser = serial.Serial("/dev/ttyAMA5", 9600, timeout=1)
            for v in values:
                ser.write(v.encode('utf-8') + b"\n")
            ser.close()
            QMessageBox.information(self, "成功", "資料已傳送")
        except Exception as e:
            QMessageBox.critical(self, "錯誤", f"無法開啟串口: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SerialSender()
    window.show()
    sys.exit(app.exec_())
