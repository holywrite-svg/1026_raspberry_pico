"""
快速 MQTT 測試腳本
快速發送測試訊息到 Streamlit 應用程式
"""

import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime

# MQTT 設定
MQTT_BROKER = "192.168.0.252"
MQTT_PORT = 1883
MQTT_USERNAME = "pi"
MQTT_PASSWORD = "raspberry"

def quick_test():
    """快速測試：發送電燈和感測器數據"""
    print("="*50)
    print("快速 MQTT 測試")
    print("="*50)
    
    # 連接 MQTT
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        time.sleep(1)
        print("✅ 已連接到 MQTT Broker\n")
    except Exception as e:
        print(f"❌ 連接失敗: {e}")
        return
    
    # 測試 1: 電燈開啟
    print("📤 發送電燈狀態: 開啟")
    data = {
        "status": "on",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    client.publish("客廳/light", json.dumps(data, ensure_ascii=False), qos=1)
    time.sleep(0.5)
    
    # 測試 2: 感測器數據
    print("📤 發送感測器數據: 溫度 25.5°C, 濕度 60%")
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": 25.5,
        "humidity": 60.0,
        "status": "正常"
    }
    client.publish("客廳/sensor", json.dumps(data, ensure_ascii=False), qos=1)
    time.sleep(0.5)
    
    # 測試 3: 連續發送 5 筆感測器數據（用於測試圖表）
    print("\n📤 連續發送 5 筆感測器數據（測試圖表）...")
    import random
    for i in range(5):
        data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "temperature": round(20 + i * 0.5 + random.uniform(-0.5, 0.5), 1),
            "humidity": round(50 + i * 2 + random.uniform(-2, 2), 1),
            "status": "正常"
        }
        client.publish("客廳/sensor", json.dumps(data, ensure_ascii=False), qos=1)
        print(f"  [{i+1}/5] 溫度: {data['temperature']}°C, 濕度: {data['humidity']}%")
        time.sleep(1)
    
    # 測試 4: 電燈關閉
    print("\n📤 發送電燈狀態: 關閉")
    data = {
        "status": "off",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    client.publish("客廳/light", json.dumps(data, ensure_ascii=False), qos=1)
    
    print("\n✅ 測試完成！請檢查 Streamlit 應用程式是否收到數據")
    
    # 斷開連接
    time.sleep(1)
    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
    quick_test()

