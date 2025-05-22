# 匯入 HelloWorldCheck 類別，來做輸入內容的檢查
from HelloWorldCheck import HelloWorldCheck

# 定義一個類別 HelloWorldOutput，負責印出結果
class HelloWorldOutput:
    
    # 定義一個方法 output_check_hello_world
    # 用來根據輸入的內容決定要印什麼
    def output_check_hello_world(self):
        check = HelloWorldCheck()  # 建立檢查器物件
        if check.check_hello_world():  # 如果使用者輸入的是 "Hello"
            print("Hello, World!")     # 印出歡迎訊息
        else:
            print("你輸入的不是Hello")  # 輸入錯誤時的提示

# 主程式入口（這段只會在執行這支檔案時執行，不會在被匯入時執行）
if __name__ == "__main__":
    output = HelloWorldOutput()             # 建立輸出處理物件
    output.output_check_hello_world()       # 執行輸出結果
