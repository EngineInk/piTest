# 匯入 HelloWorldInput 類別（從 HelloWorldInput.py 檔案中）
from HelloWorldInput import HelloWorldInput

# 定義一個類別 HelloWorldCheck，用來檢查使用者輸入的內容
class HelloWorldCheck:

    # 建構子，當物件被建立時自動執行
    def __init__(self):
        # 建立 HelloWorldInput 的物件，並呼叫它來取得使用者輸入
        self.hwi = HelloWorldInput()
        self.hwi.get_input_world()  # 顯示提示訊息並取得輸入

    # 定義一個方法 check_hello_world，用來檢查輸入是否為 "Hello"
    def check_hello_world(self):
        # 從 hwi（HelloWorldInput 的物件）取得使用者輸入
        # 並檢查是否等於 "Hello"，結果為 True 或 False
        return self.hwi.return_input_world() == "Hello"
