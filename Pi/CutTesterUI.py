import sys
import os
import PyQt5
import random
import time
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QVBoxLayout, QGridLayout,
    QLabel, QPlainTextEdit, QLineEdit, QFrame,
    QPushButton
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QPen, QColor

# 設定 PyQt5 插件路徑
dirname = os.path.dirname(PyQt5.__file__)
plugin_path = os.path.join(dirname, 'Qt5', 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

class DrawingArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.border_points = []  # 儲存邊框和格線的點
        self.random_points = []  # 儲存隨機生成的點
        self.setMinimumSize(236,420)  
        self.setSizePolicy(
            PyQt5.QtWidgets.QSizePolicy.Expanding,
            PyQt5.QtWidgets.QSizePolicy.Expanding
        )
        # 設定座標範圍
        self.x_min = 0
        self.x_max = 100
        self.y_min = 0
        self.y_max = 100
        
        # 初始化時繪製邊框
        self.draw_border()
        
    def draw_border(self):
        """繪製邊框點"""
        # 清除現有的點
        self.border_points = []
        
        step = 0.1  # 使用更小的步進值，讓點更密集
        
        # 底部橫線 (0,0) 到 (100,0)
        x = 0
        while x <= 100:
            self.border_points.append((x, 0))
            x += step
            
        # 右側直線 (100,0) 到 (100,100)
        y = 0
        while y <= 100:
            self.border_points.append((100, y))
            y += step
            
        # 頂部橫線 (100,100) 到 (0,100)
        x = 100
        while x >= 0:
            self.border_points.append((x, 100))
            x -= step
            
        # 左側直線 (0,100) 到 (0,0)
        y = 100
        while y >= 0:
            self.border_points.append((0, y))
            y -= step
            
        # 繪製格線
        self.draw_grid()
            
        self.update()
        
    def draw_grid(self):
        """繪製10等分格線"""
        step = 0.1  # 點的間隔
        
        # 繪製垂直線（x軸方向的分隔）
        for i in range(1, 10):  # 1到9，因為0和10是邊框
            x = i * 10  # 每10個單位一條線
            y = 0
            while y <= 100:
                self.border_points.append((x, y))
                y += step
                
        # 繪製水平線（y軸方向的分隔）
        for i in range(1, 10):  # 1到9，因為0和10是邊框
            y = i * 10  # 每10個單位一條線
            x = 0
            while x <= 100:
                self.border_points.append((x, y))
                x += step
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 設定外框
        margin = 10  # 外框和內容的間距
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor('#E8E8E8'))  # 淺灰色背景
        painter.drawRoundedRect(self.rect(), 12, 12)  # 繪製圓角矩形外框
        
        # 計算內部繪圖區域
        inner_rect = self.rect().adjusted(margin, margin, -margin, -margin)
        
        # 設定內部白色背景
        painter.setBrush(QColor('#FFFFFF'))
        painter.drawRect(inner_rect)
        
        # 保存當前狀態
        painter.save()
        # 設定裁剪區域為內部矩形
        painter.setClipRect(inner_rect)
        
        # 繪製邊框和格線（灰色）
        self.draw_border_and_grid(painter)
        
        # 繪製隨機點（紅色）
        self.draw_random_point(painter)
        
        # 恢復繪圖狀態
        painter.restore()

    def draw_border_and_grid(self, painter):
        """繪製邊框和格線"""
        if self.border_points:
            pen = QPen(QColor('#999999'))
            pen.setWidth(2)
            painter.setPen(pen)
            for x, y in self.border_points:
                screen_x = self.to_screen_x(x)
                screen_y = self.to_screen_y(y)
                painter.drawPoint(screen_x, screen_y)

    def draw_random_point(self, painter):
        """繪製隨機點"""
        if self.random_points:
            pen = QPen(QColor('#FF0000'))
            pen.setWidth(4)
            painter.setPen(pen)
            for x, y in self.random_points:
                screen_x = self.to_screen_x(x)
                screen_y = self.to_screen_y(y)
                painter.drawPoint(screen_x, screen_y)
    
    def to_screen_x(self, x):
        """將X數據座標轉換為螢幕座標，考慮邊距"""
        margin = 10
        w = self.width() - 2 * margin
        return int(margin + (x - self.x_min) * w / (self.x_max - self.x_min))
    
    def to_screen_y(self, y):
        """將Y數據座標轉換為螢幕座標，考慮邊距"""
        margin = 10
        h = self.height() - 2 * margin
        # Y軸從下往上，所以y值越大，螢幕座標越小
        return int(self.height() - margin - (y - self.y_min) * h / (self.y_max - self.y_min))
    
    def add_point(self, x, y):
        """添加新的點"""
        self.random_points.append((x, y))
        self.update()
    
    def clear_points(self):
        """清除所有點"""
        self.random_points = []
        self.update()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cut Tester")
        self.resize(900, 300)
        
        # 控制變數
        self.is_running = False
        self.received_coordinates = None  # 用於存儲接收到的座標
        
        # 建立中央容器
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 創建主垂直布局
        main_vertical_layout = QVBoxLayout(central_widget)
        
        # 創建上方內容的水平布局
        top_content_layout = QHBoxLayout()
        top_content_layout.setSpacing(10)  # 設置佈局元件之間的間距

        # ---------------------
        # 左側單欄（9 個區塊）
        # ---------------------
        left_layout = QVBoxLayout()
        
        # 第一列
        row_layout = QHBoxLayout()
        label_name1 = QLabel("name1")
        label_name1.setAlignment(Qt.AlignCenter)
        label_name1.setFixedWidth(100)
        
        input_value1 = QLineEdit()
        input_value1.setAlignment(Qt.AlignCenter)
        input_value1.setFixedWidth(150)
        input_value1.setPlaceholderText("0,0")
        
        row_layout.addWidget(label_name1)
        row_layout.addWidget(input_value1)
        left_layout.addLayout(row_layout)
        
        # 第二列
        row_layout = QHBoxLayout()
        label_name2 = QLabel("name2")
        label_name2.setAlignment(Qt.AlignCenter)
        label_name2.setFixedWidth(100)
        
        input_value2 = QLineEdit()
        input_value2.setAlignment(Qt.AlignCenter)
        input_value2.setFixedWidth(150)
        input_value2.setPlaceholderText("0,0")
        
        row_layout.addWidget(label_name2)
        row_layout.addWidget(input_value2)
        left_layout.addLayout(row_layout)
        
        # 第三列
        row_layout = QHBoxLayout()
        label_name3 = QLabel("name3")
        label_name3.setAlignment(Qt.AlignCenter)
        label_name3.setFixedWidth(100)
        
        input_value3 = QLineEdit()
        input_value3.setAlignment(Qt.AlignCenter)
        input_value3.setFixedWidth(150)
        input_value3.setPlaceholderText("0")
        
        row_layout.addWidget(label_name3)
        row_layout.addWidget(input_value3)
        left_layout.addLayout(row_layout)
        
        # 第四列
        row_layout = QHBoxLayout()
        label_name4 = QLabel("name4")
        label_name4.setAlignment(Qt.AlignCenter)
        label_name4.setFixedWidth(100)
        
        input_value4 = QLineEdit()
        input_value4.setAlignment(Qt.AlignCenter)
        input_value4.setFixedWidth(150)
        input_value4.setPlaceholderText("0")
        
        row_layout.addWidget(label_name4)
        row_layout.addWidget(input_value4)
        left_layout.addLayout(row_layout)
        
        # 第五列
        row_layout = QHBoxLayout()
        label_name5 = QLabel("name5")
        label_name5.setAlignment(Qt.AlignCenter)
        label_name5.setFixedWidth(100)
        
        input_value5 = QLineEdit()
        input_value5.setAlignment(Qt.AlignCenter)
        input_value5.setFixedWidth(150)
        input_value5.setPlaceholderText("0")
        
        row_layout.addWidget(label_name5)
        row_layout.addWidget(input_value5)
        left_layout.addLayout(row_layout)
        
        # 第六列
        row_layout = QHBoxLayout()
        label_name6 = QLabel("name6")
        label_name6.setAlignment(Qt.AlignCenter)
        label_name6.setFixedWidth(100)
        
        input_value6 = QLineEdit()
        input_value6.setAlignment(Qt.AlignCenter)
        input_value6.setFixedWidth(150)
        input_value6.setPlaceholderText("0")
        
        row_layout.addWidget(label_name6)
        row_layout.addWidget(input_value6)
        left_layout.addLayout(row_layout)
        
        # 第七列
        row_layout = QHBoxLayout()
        label_name7 = QLabel("name7")
        label_name7.setAlignment(Qt.AlignCenter)
        label_name7.setFixedWidth(100)
        
        input_value7 = QLineEdit()
        input_value7.setAlignment(Qt.AlignCenter)
        input_value7.setFixedWidth(150)
        input_value7.setPlaceholderText("0")
        
        row_layout.addWidget(label_name7)
        row_layout.addWidget(input_value7)
        left_layout.addLayout(row_layout)
        
        # 第八列
        row_layout = QHBoxLayout()
        label_name8 = QLabel("name8")
        label_name8.setAlignment(Qt.AlignCenter)
        label_name8.setFixedWidth(100)
        
        input_value8 = QLineEdit()
        input_value8.setAlignment(Qt.AlignCenter)
        input_value8.setFixedWidth(150)
        input_value8.setPlaceholderText("0")
        
        row_layout.addWidget(label_name8)
        row_layout.addWidget(input_value8)
        left_layout.addLayout(row_layout)
        
        # 第九列
        row_layout = QHBoxLayout()
        label_name9 = QLabel("name9")
        label_name9.setAlignment(Qt.AlignCenter)
        label_name9.setFixedWidth(100)
        
        input_value9 = QLineEdit()
        input_value9.setAlignment(Qt.AlignCenter)
        input_value9.setFixedWidth(150)
        input_value9.setPlaceholderText("0")
        
        row_layout.addWidget(label_name9)
        row_layout.addWidget(input_value9)
        left_layout.addLayout(row_layout)

        # 將這些輸入框保存為類的屬性，以便後續訪問
        self.input_values = {
            'name1': input_value1,
            'name2': input_value2,
            'name3': input_value3,
            'name4': input_value4,
            'name5': input_value5,
            'name6': input_value6,
            'name7': input_value7,
            'name8': input_value8,
            'name9': input_value9
        }

        # 將左側區塊加到上方內容布局
        top_content_layout.addLayout(left_layout)

        # 添加垂直分隔線
        vertical_line = QFrame()
        vertical_line.setFrameShape(QFrame.VLine)
        vertical_line.setFrameShadow(QFrame.Sunken)
        vertical_line.setStyleSheet("""
            QFrame { 
                background-color: #666666; 
                margin-left: 15px;
                margin-right: 15px;
                margin-top: 5px;
                margin-bottom: 5px;
            }
        """)
        top_content_layout.addWidget(vertical_line)

        # ---------------------
        # 右側：大區域 + 底部資訊
        # ---------------------
        right_layout = QVBoxLayout()
        right_layout.setStretch(0, 8)  # 增加繪圖區域的比例
        right_layout.setStretch(1, 1)  # 底部區域比例保持不變

        # 大區域：改為繪圖區域
        self.drawing_area = DrawingArea()
        right_layout.addWidget(self.drawing_area)

        # 底部資訊：水平放置 2 組 (最大誤差 / 0) 與 (name01 / 0)
        bottom_layout = QHBoxLayout()

        # 左小塊
        box_left_layout = QVBoxLayout()
        label_max_error = QLabel("最大誤差")
        label_max_error.setAlignment(Qt.AlignCenter)
        input_max_error = QLineEdit()
        input_max_error.setAlignment(Qt.AlignCenter)
        input_max_error.setPlaceholderText("0")  # 設定預設提示文字
        box_left_layout.addWidget(label_max_error)
        box_left_layout.addWidget(input_max_error)

        # 右小塊
        box_right_layout = QVBoxLayout()
        label_name01 = QLabel("name01")
        label_name01.setAlignment(Qt.AlignCenter)
        input_name01 = QLineEdit()
        input_name01.setAlignment(Qt.AlignCenter)
        input_name01.setPlaceholderText("0")  # 設定預設提示文字
        box_right_layout.addWidget(label_name01)
        box_right_layout.addWidget(input_name01)

        bottom_layout.addLayout(box_left_layout)
        bottom_layout.addLayout(box_right_layout)

        # 將底部資訊加到右側區塊
        right_layout.addLayout(bottom_layout)

        # 將右側區塊加到上方內容布局
        top_content_layout.addLayout(right_layout)

        # 將上方內容布局加入主垂直布局
        main_vertical_layout.addLayout(top_content_layout)

        # 添加水平分隔線
        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setFrameShadow(QFrame.Sunken)
        horizontal_line.setFixedHeight(2)  # 設定分隔線本身高度為2px
        horizontal_line.setStyleSheet("""
            QFrame { 
                background-color: #666666; 
                margin: 0px;
            }
        """)
        # 添加間距
        spacer_top = QWidget()
        spacer_top.setFixedHeight(5)  # 上方間距改為20px
        spacer_bottom = QWidget()
        spacer_bottom.setFixedHeight(5)  # 下方間距改為20px
        
        main_vertical_layout.addWidget(spacer_top)
        main_vertical_layout.addWidget(horizontal_line)
        main_vertical_layout.addWidget(spacer_bottom)

        # 添加 RUN/STOP 按鈕到底部
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0,0,0,0)  # 設置左右和底部邊距
        button_layout.setSpacing(10)  # 設置按鈕之間的間距
        
        run_button = QPushButton("RUN")
        run_button.setFixedHeight(50)  # 設置按鈕高度
        run_button.setObjectName("runButton")
        run_button.clicked.connect(self.start_generation)
        
        stop_button = QPushButton("STOP")
        stop_button.setFixedHeight(50)  # 設置按鈕高度
        stop_button.setObjectName("stopButton")
        stop_button.clicked.connect(self.stop_generation)
        
        # 設置按鈕寬度比例為 2:1
        button_layout.addWidget(run_button, 2)  # 佔用 2 份寬度
        button_layout.addWidget(stop_button, 1)  # 佔用 1 份寬度
        
        # 將按鈕布局加入主垂直布局
        main_vertical_layout.addLayout(button_layout)

        # ---------------------
        # 設定整體樣式
        # ---------------------
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #222222;       /* 整體背景 */
            }
            QLabel {
                background-color: #777777;       /* 左側區塊的背景 */
                color: #ffffff;                  /* 文字顏色 */
                padding: 8px;
                font-size: 14px;
                font-weight: bold;              /* 粗體字 */
                border-radius: 8px;             /* 添加圓角 */
            }
            QLineEdit {
                background-color: #E8E8E8;       /* 輸入框淺灰色背景 */
                color: #000000;                  /* 文字顏色 */
                padding: 8px;
                font-size: 14px;
                font-weight: bold;              /* 粗體字 */
                border-radius: 8px;             /* 添加圓角 */
            }
            QLineEdit::placeholder {
                color: #999999;                  /* 預設提示文字顏色 */
                font-weight: bold;              /* 粗體字 */
            }
            DrawingArea {
                background-color: #FFFFFF;       /* 繪圖區白底 */
                border: 2px solid #AA00FF;       /* 紫色邊框 */
                border-radius: 12px;            /* 添加圓角 */
            }
            QPushButton#runButton {
                background-color: #2ECC71;      /* 綠色背景 */
                color: #FFFFFF;                 /* 文字顏色 */
                border: none;
                border-radius: 8px;            /* 按鈕圓角 */
                font-size: 18px;               /* 加大字體 */
                font-weight: bold;             /* 粗體字 */
            }
            QPushButton#stopButton {
                background-color: #E74C3C;      /* 紅色背景 */
                color: #FFFFFF;                 /* 文字顏色 */
                border: none;
                border-radius: 8px;            /* 按鈕圓角 */
                font-size: 18px;               /* 加大字體 */
                font-weight: bold;             /* 粗體字 */
            }
            QPushButton#runButton:hover {
                background-color: #27AE60;      /* 滑鼠懸停時的深綠色 */
            }
            QPushButton#stopButton:hover {
                background-color: #C0392B;      /* 滑鼠懸停時的深紅色 */
            }
            QPushButton#runButton:pressed {
                background-color: #229954;      /* 按下時的更深綠色 */
            }
            QPushButton#stopButton:pressed {
                background-color: #A93226;      /* 按下時的更深紅色 */
            }
        """)

    def receive_coordinates(self):
        """模擬接收座標的函數，之後可以替換為實際的接收邏輯"""
        # TODO: 替換為實際的座標接收邏輯
        if self.is_running:
            return random.uniform(0, 100), random.uniform(0, 100)
        return None
        
    def update_display(self, x, y):
        """更新顯示"""
        self.drawing_area.add_point(x, y)
        # TODO: 在這裡添加更新其他數值的邏輯
        
    def start_generation(self):
        """開始接收座標"""
        self.is_running = True
        self.drawing_area.clear_points()  # 清除之前的點
        
    def stop_generation(self):
        """停止接收座標"""
        self.is_running = False

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    # 主循環
    while True:
        app.processEvents()  # 處理Qt事件
        
        # 嘗試接收座標
        coordinates = window.receive_coordinates()
        
        # 如果接收到座標，則更新顯示
        if coordinates:
            x, y = coordinates
            window.update_display(x, y)
        
        time.sleep(0.05)  # 適當的休眠以減少CPU使用率

if __name__ == "__main__":
    main()
