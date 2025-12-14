from machine import ADC, Pin
import time

# 溫度感測器連接到 ADC 4，但在 MicroPython 中，我們通常直接使用 4 作為 Pin 腳位編號
# 或者使用特定於 Pico SDK 的方式來初始化
# 在大多數 MicroPython 版本中，ADC(4) 即代表內部溫度感測器
sensor_temp = ADC(4)

# 類比數位轉換器 ADC 的參考電壓 (Reference Voltage)
# Pico 的 ADC 是 12 bit，最大值為 2^12 - 1 = 4095
conversion_factor = 3.3 / (65535) # 由於 MicroPython 預設讀取 16 位元 (0-65535)，所以使用 65535

def read_temperature():
    """讀取並轉換 RP2040 晶片內建溫度感測器的值"""
    
    # 讀取 ADC 的原始 16 位元值 (0-65535)
    reading = sensor_temp.read_u16() 
    
    # 步驟 1: 將 16 位元讀數轉換回實際電壓值
    voltage = reading * conversion_factor
    
    # 步驟 2: 使用官方資料表提供的公式將電壓轉換為攝氏溫度 (°C)
    # 根據 Raspberry Pi Pico SDK 文件，公式為：
    # 溫度 = 27 - (ADC_電壓 - 0.706) / 0.001721
    temperature = 27 - (voltage - 0.706) / 0.001721
    
    return temperature

# --- 主迴圈 ---
print("開始讀取 Pico W 晶片溫度...")

while True:
    temp_c = read_temperature()
    
    # 格式化輸出，保留兩位小數
    print(f"晶片溫度: {temp_c:.2f} °C")
    
    time.sleep(2) # 每 2 秒讀取一次