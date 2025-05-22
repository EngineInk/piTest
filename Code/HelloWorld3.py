
#把ABC的內容  改為  你接下輸入的內容   在顯示"請輸入Hello:"之後 
# ABC          =    input(            "請輸入Hello: ")

ABC = input("請輸入Hello: ")



# 如果   ABC的內容  剛好是  "Hello"
# if     ABC        ==     "Hello":
if ABC == "Hello":   
    print("Hello, World!")
    #印出("你的輸入:"+ ABC的內容)

# 否則:
else:
    print("你輸入的是:", ABC, "不是Hello")
    #印出("你的輸入:" "ABC的內容" "不是Hello")
