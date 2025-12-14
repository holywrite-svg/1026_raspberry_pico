from machine import Pin
from time import sleep

# --- GPIO 腳位設定 ---
btn_pin = 14
led_pin = 15

# --- 變數初始化 ---
# 追蹤 LED 的目前狀態 (True=ON, False=OFF)。初始設定為 OFF (False)
led_state = False 
# 追蹤按鈕的上次讀取值。使用 PULL_UP，所以初始狀態是 1 (未按下)
last_button_state = 1 

# --- 硬體初始化 ---
# 按鈕：Pin.IN (輸入), Pin.PULL_UP (上拉電阻)
#   - 未按下: value() == 1
#   - 按下: value() == 0 
button = Pin(btn_pin, Pin.IN, Pin.PULL_UP)

# LED：Pin.OUT (輸出)
led = Pin(led_pin, Pin.OUT)

# 確保 LED 初始狀態與變數一致
led.value(led_state) 

print("啟動切換開關模式...")

# --- 主迴圈 ---
while True:
    # 1. 讀取當前按鈕狀態
    current_button_state = button.value()
    
    # 2. 判斷按鍵是否被「按下」且是「新的按下事件」(狀態由 1 變為 0)
    # 這是實現去彈跳和單次觸發的核心邏輯
    if current_button_state == 0 and last_button_state == 1:
        # 當檢測到從未按 (1) 轉換到按下 (0) 的瞬間：
        
        # A. 反轉 LED 狀態 (True 變 False，False 變 True)
        led_state = not led_state 
        
        # B. 根據新的狀態控制 LED
        led.value(led_state)
        
        # C. 為了防止在按住期間重複觸發，加入短暫延遲 (軟體去彈跳)
        sleep(0.05) # 50 毫秒延遲
        
        if led_state:
            print("LED ON")
        else:
            print("LED OFF")
    
    # 3. 更新上次狀態
    # 將當前的按鈕狀態存起來，供下一次迴圈使用
    last_button_state = current_button_state
    
    # 休息一下以節省 CPU 資源
    sleep(0.01) # 10 毫秒