from machine import Pin
import time

# 設置 GPIO 15 為輸出引腳
led_pin = Pin(15, Pin.OUT)

print("開始閃爍 GPIO 15 上的 LED...")

# 讓 LED 持續閃爍
while True:
    # 點亮 LED (高電平)
    led_pin.value(1)
    print("LED ON")
    time.sleep(0.5)  # 暫停 0.5 秒

    # 熄滅 LED (低電平)
    led_pin.value(0)
    print("LED OFF")
    time.sleep(0.5)  # 暫停 0.5 秒