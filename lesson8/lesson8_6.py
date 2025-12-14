from machine import Pin, ADC, PWM
import time

# --- 硬體初始化 ---
# 可變電阻，連接到 GP26
potentiometer = ADC(Pin(28))

# LED，使用 PWM 控制，連接到 GP15
led_pwm = PWM(Pin(15))
led_pwm.freq(1000)  # 設定 PWM 頻率為 1000Hz

# 按鈕，連接到 GP14，使用內部上拉電阻
button = Pin(14, Pin.IN, Pin.PULL_UP)

# --- 狀態與中斷防彈跳變數 ---
led_is_on = False  # LED 的開關狀態
last_interrupt_time = 0  # 上次中斷觸發時間

# --- 中斷處理函式 (ISR) ---
def button_irq_handler(pin):
    """當中斷觸發時，切換 LED 的開關狀態"""
    global led_is_on, last_interrupt_time
    current_time = time.ticks_ms()

    # 軟體防彈跳：與上次觸發時間間隔需大於 200ms
    if time.ticks_diff(current_time, last_interrupt_time) > 200:
        last_interrupt_time = current_time
        led_is_on = not led_is_on  # 反轉開關狀態
        print(f"IRQ: LED toggled to {'ON' if led_is_on else 'OFF'}")

# --- 註冊中斷 ---
# 設定按鈕在下降邊緣 (按下瞬間) 觸發中斷
button.irq(trigger=Pin.IRQ_FALLING, handler=button_irq_handler)

print("可調光開關已啟動 (中斷模式)...")

# --- 主迴圈 ---
while True:
    if led_is_on:
        # 如果 LED 是開啟狀態，則讀取可變電阻並設定亮度
        brightness = potentiometer.read_u16()
        led_pwm.duty_u16(brightness)
    else:
        # 如果 LED 是關閉狀態，則將亮度設為 0
        led_pwm.duty_u16(0)

    # 短暫延遲以降低 CPU 負載
    time.sleep_ms(20)