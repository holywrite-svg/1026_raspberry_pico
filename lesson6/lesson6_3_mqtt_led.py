'''
MQTT 訂閱程式 - 收到訊息時 LED 亮 0.1 秒
適用於 Raspberry Pi Pico W
'''

from machine import Pin, Timer
import binascii
import time
import machine
import network
from umqtt.simple import MQTTClient

# WiFi 設定（請修改為您的 WiFi 資訊）
WIFI_SSID = "F602-15D"  # 請修改
WIFI_PASSWORD = "raspberry"  # 請修改

# MQTT 設定
MQTT_SERVER = "localhost"
MQTT_PORT = 1883
MQTT_USERNAME = "pi"
MQTT_PASSWORD = "raspberry"
MQTT_TOPIC = "客廳/message"  # 訂閱的主題，可以改為 "客廳/#" 訂閱所有

# LED 設定
led = Pin("LED", Pin.OUT)  # 使用內建 LED，或改為 Pin(15, Pin.OUT) 使用外部 LED
led.off()  # 初始狀態關閉

# Timer 用於控制 LED 關閉時間
led_timer = None

def turn_off_led(timer):
    '''Timer 回調函數：關閉 LED'''
    global led
    led.off()
    print("LED 已關閉")

def blink_led(duration_ms=100):
    '''
    讓 LED 亮指定時間後自動關閉
    :param duration_ms: LED 亮的時間（毫秒），預設 100ms (0.1秒)
    '''
    global led, led_timer
    
    # 如果已經有 Timer 在運行，先取消
    if led_timer:
        led_timer.deinit()
    
    # 開啟 LED
    led.on()
    print(f"💡 LED 已開啟，將在 {duration_ms}ms 後關閉")
    
    # 建立 Timer 在指定時間後關閉 LED
    led_timer = Timer()
    led_timer.init(mode=Timer.ONE_SHOT, period=duration_ms, callback=turn_off_led)

def mqtt_callback(topic, msg):
    '''
    MQTT 訊息接收回調函數
    :param topic: 主題（bytes）
    :param msg: 訊息內容（bytes）
    '''
    topic_str = topic.decode('utf-8')
    msg_str = msg.decode('utf-8')
    
    print(f"\n📨 收到 MQTT 訊息:")
    print(f"   主題: {topic_str}")
    print(f"   內容: {msg_str}")
    
    # 收到訊息時，讓 LED 亮 0.1 秒
    blink_led(100)  # 100 毫秒 = 0.1 秒

def connect_wifi(ssid, password):
    '''
    連接 WiFi
    :param ssid: WiFi 名稱
    :param password: WiFi 密碼
    :return: True 如果連接成功，False 如果失敗
    '''
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print(f"正在連接 WiFi: {ssid}...")
        wlan.connect(ssid, password)
        
        # 等待連接，最多等待 10 秒
        max_wait = 10
        while max_wait > 0:
            if wlan.isconnected():
                break
            max_wait -= 1
            print(".", end="")
            time.sleep(1)
        
        if wlan.isconnected():
            print("\n✅ WiFi 連接成功!")
            print(f"   IP 位址: {wlan.ifconfig()[0]}")
            return True
        else:
            print("\n❌ WiFi 連接失敗!")
            return False
    else:
        print("✅ WiFi 已連接!")
        print(f"   IP 位址: {wlan.ifconfig()[0]}")
        return True

def main():
    global mqtt_client
    
    print("=" * 50)
    print("MQTT LED 控制程式")
    print("=" * 50)
    
    # 1. 連接 WiFi
    print("\n[1/3] 正在連接 WiFi...")
    if not connect_wifi(WIFI_SSID, WIFI_PASSWORD):
        print("❌ 無法連接 WiFi，程式結束")
        return
    
    # 2. 連接 MQTT Broker
    print(f"\n[2/3] 正在連接 MQTT Broker ({MQTT_SERVER}:{MQTT_PORT})...")
    try:
        client_id = binascii.hexlify(machine.unique_id())
        mqtt_client = MQTTClient(client_id, MQTT_SERVER, 
                                 user=MQTT_USERNAME, 
                                 password=MQTT_PASSWORD)
        mqtt_client.set_callback(mqtt_callback)  # 設定訊息接收回調
        mqtt_client.connect()
        print("✅ MQTT 連接成功!")
    except Exception as e:
        print(f"❌ MQTT 連接失敗: {e}")
        return
    
    # 3. 訂閱主題
    print(f"\n[3/3] 正在訂閱主題: {MQTT_TOPIC}")
    try:
        mqtt_client.subscribe(MQTT_TOPIC.encode('utf-8'))
        print(f"✅ 已訂閱主題: {MQTT_TOPIC}")
        print("\n" + "=" * 50)
        print("✅ 程式已啟動，等待接收 MQTT 訊息...")
        print("   當收到訊息時，LED 會亮 0.1 秒")
        print("   按 Ctrl+C 停止程式")
        print("=" * 50 + "\n")
    except Exception as e:
        print(f"❌ 訂閱失敗: {e}")
        return
    
    # 4. 持續監聽訊息
    try:
        while True:
            # 檢查是否有新訊息（非阻塞）
            mqtt_client.check_msg()
            # 短暫延遲，避免 CPU 使用率過高
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\n⚠️  程式被中斷")
    finally:
        # 清理資源
        print("\n正在清理資源...")
        if led_timer:
            led_timer.deinit()
        led.off()
        mqtt_client.disconnect()
        print("✅ 已斷開 MQTT 連線")
        print("✅ 程式已結束")

if __name__ == '__main__':
    main()

