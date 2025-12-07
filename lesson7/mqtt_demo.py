# mqtt_demo.py
# 適用：Raspberry Pi Pico W (MicroPython)
# 需確認已安裝 umqtt.simple (通常透過 Thonny 的套件管理搜尋 micropython-umqtt.simple 安裝)

import time
from umqtt.simple import MQTTClient
import wifi_connect
import ubinascii
import machine

# -------------------------------
# MQTT 設定
# -------------------------------
# ⚠️ 重要：請將此 IP 改為您電腦(Broker)的區域網路 IP
# 在 Windows 開 cmd 輸入 ipconfig 查看 IPv4 位址
MQTT_BROKER = "10.218.58.186" 
MQTT_PORT = 1883
MQTT_USER = ""        # 如果 Broker 有設定帳號密碼請填寫
MQTT_PASSWORD = ""

# 產生唯一的 Client ID
CLIENT_ID = ubinascii.hexlify(machine.unique_id())

# 主題設定
TOPIC_PUB = b"pico/data"      # Pico 發送數據的主題
TOPIC_SUB = b"pico/command"   # Pico 接收指令的主題

# 一閃一閃亮晶晶的節奏 (時間單位: 秒)
# 1 = 亮, 0 = 暗, 0.5 = 持續時間
TWINKLE_RHYTHM = [
    (1, 0.5), (0, 0.5), (1, 0.5), (0, 0.5), (1, 0.5), (0, 0.5), (1, 1.0), # 一閃一閃亮晶晶
    (0, 0.5), (1, 0.5), (0, 0.5), (1, 0.5), (0, 0.5), (1, 0.5), (0, 0.5), (1, 1.0)  # 滿天都是小星星
]

is_playing = False
current_note_index = 0
note_start_time = 0
led_pin = machine.Pin("LED", machine.Pin.OUT)

# -------------------------------
# 接收訊息的回調函式
# -------------------------------
def sub_cb(topic, msg):
    print(f"\n收到訊息 -> 主題: {topic.decode()}, 內容: {msg.decode()}")
    
    # 範例：收到 "on" 開燈 (啟動一閃一閃亮晶晶模式)
    if msg == b"on":
        global is_playing
        is_playing = True
        print("🎵 啟動音樂燈光模式: 一閃一閃亮晶晶")
        
    elif msg == b"off":
        global is_playing
        is_playing = False
        machine.Pin("LED", machine.Pin.OUT).off()
        print("LED 已關閉")

# -------------------------------
# 主程式
# -------------------------------
def main():
    # 1. 連接 WiFi
    wlan = wifi_connect.connect()
    if not wlan.isconnected():
        print("無法連上網路，程式終止")
        return

    print(f"正在連接 MQTT Broker ({MQTT_BROKER})...")
    
    try:
        # 2. 初始化 MQTT Client
        client = MQTTClient(
            CLIENT_ID, 
            MQTT_BROKER, 
            port=MQTT_PORT, 
            user=MQTT_USER, 
            password=MQTT_PASSWORD,
            keepalive=60
        )
        
        # 設定回調函式 (收到訊息時會執行)
        client.set_callback(sub_cb)
        
        # 建立連線
        client.connect()
        print("✅ MQTT 連線成功!")
        
        # 3. 訂閱主題
        client.subscribe(TOPIC_SUB)
        print(f"已訂閱主題: {TOPIC_SUB.decode()}")
        
        # 4. 主迴圈
    top_is_playing = False
    top_current_note_index = 0
    top_note_start_time = 0

    # 4. 主迴圈
    last_pub = time.ticks_ms()
    counter = 0

    while True:
        # 保持監聽 (每圈都要執行)
        client.check_msg()

        # 檢查時間是否超過 10 秒 (10000 ms)
        now = time.ticks_ms()
        if time.ticks_diff(now, last_pub) >= 10000:
            msg = f"Data #{counter} from Pico"
            client.publish(TOPIC_PUB, msg)
            print(f"[{counter}] 已發送: {msg}")

            counter += 1
            last_pub = now

        # --- 處理 LED 音樂燈光 (非阻塞) ---
        # 為了避免與函數內的變數混淆，我們直接使用 global 的變數狀態
        # 注意：Python 中如果在函數內對全域變數賦值，需要宣告 global
        # 但如果是讀取則不需要，不過為了保險起見，我們統一處理
        
        global is_playing, current_note_index, note_start_time

        if is_playing:
            # 取得目前音符 (狀態, 持續時間)
            state, duration = TWINKLE_RHYTHM[current_note_index]

            # 設定 LED 狀態
            if state:
                led_pin.on()
            else:
                led_pin.off()

            # 檢查這個音符是否播放完畢
            # duration 是秒，轉成 ms
            if time.ticks_diff(now, note_start_time) >= duration * 1000:
                current_note_index += 1
                note_start_time = now

                # 如果播完整首，重頭開始
                if current_note_index >= len(TWINKLE_RHYTHM):
                    current_note_index = 0
        else:
             # 確保停止時燈是滅的
             pass

        # 短暫休息避免 CPU 滿載，但不要睡太久以免錯過訊息
        time.sleep(0.01) 
            
    except OSError as e:
        print(f"❌ MQTT 連線或傳輸錯誤: {e}")
        if e.args[0] == 103 or e.args[0] == 113:
            print("💡 提示：'ECONNABORTED' 或 'EHOSTUNREACH' 通常代表：")
            print("1. 電腦防火牆阻擋了 1883 Port (請在防火牆新增輸入規則)")
            print("2. Mosquitto Broker 預設只監聽 localhost (需修改 mosquitto.conf 加入 'listener 1883' 和 'allow_anonymous true')")
        print("請檢查 IP 是否正確，以及 Broker 是否已啟動")
        # 斷線後重連邏輯可在此實作

if __name__ == "__main__":
    main()
