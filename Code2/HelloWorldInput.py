# 定義一個名為 HelloWorldInput 的類別，用來處理使用者輸入
class HelloWorldInput:

    # 建構子（constructor），在建立物件時自動執行
    # 初始化一個成員變數 input_world，預設是空字串
    def __init__(self):
        self.input_world = ""

    # 定義一個方法 get_input_world，用來從使用者那邊取得輸入
    def get_input_world(self):
        # 顯示提示文字並將輸入的內容儲存到 input_world 成員變數
        self.input_world = input("請輸入文字: ")

    # 定義一個方法 return_input_world，用來回傳剛剛輸入的內容
    def return_input_world(self):
        return self.input_world