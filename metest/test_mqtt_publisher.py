"""
MQTT 測試發布器
用於測試 Streamlit 應用程式是否能正確接收 MQTT 訊息
"""

import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime
import sys

# MQTT 設定（與 Streamlit 應用程式相同）
MQTT_BROKER = "localhost"  # 改為與 app.py 一致
MQTT_PORT = 1883
MQTT_USERNAME = "pi"
MQTT_PASSWORD = "raspberry"

# 主題
TOPIC_LIGHT = "客廳/light"
TOPIC_SENSOR = "客廳/sensor"

def on_connect(client, userdata, flags, rc):
    """連接成功回調"""
    if rc == 0:
        print("✅ 成功連接到 MQTT Broker!")
    else:
        print(f"❌ 連接失敗，錯誤代碼: {rc}")
        sys.exit(1)

def on_publish(client, userdata, mid):
    """發布成功回調"""
    print(f"📤 訊息已發布 (Message ID: {mid})")

def connect_mqtt():
    """連接 MQTT Broker"""
    client = mqtt.Client()
    
    if MQTT_USERNAME and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    
    client.on_connect = on_connect
    client.on_publish = on_publish
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        time.sleep(1)  # 等待連接建立
        return client
    except Exception as e:
        print(f"❌ 連接錯誤: {e}")
        sys.exit(1)

def test_light_status(client, status="on"):
    """測試電燈狀態訊息"""
    print(f"\n{'='*50}")
    print(f"測試 1: 發送電燈狀態訊息 (狀態: {status})")
    print(f"{'='*50}")
    
    data = {
        "status": status,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    message = json.dumps(data, ensure_ascii=False)
    result = client.publish(TOPIC_LIGHT, message, qos=1)
    
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print(f"✅ 發布成功!")
        print(f"   主題: {TOPIC_LIGHT}")
        print(f"   訊息: {message}")
    else:
        print(f"❌ 發布失敗，錯誤代碼: {result.rc}")
    
    return result.rc == mqtt.MQTT_ERR_SUCCESS

def test_sensor_data(client, temperature=25.5, humidity=60.0):
    """測試感測器數據訊息"""
    print(f"\n{'='*50}")
    print(f"測試 2: 發送感測器數據")
    print(f"{'='*50}")
    
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": temperature,
        "humidity": humidity,
        "status": "正常"
    }
    
    message = json.dumps(data, ensure_ascii=False)
    result = client.publish(TOPIC_SENSOR, message, qos=1)
    
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print(f"✅ 發布成功!")
        print(f"   主題: {TOPIC_SENSOR}")
        print(f"   訊息: {message}")
    else:
        print(f"❌ 發布失敗，錯誤代碼: {result.rc}")
    
    return result.rc == mqtt.MQTT_ERR_SUCCESS

def test_continuous_sensor_data(client, count=10, interval=2):
    """連續發送多筆感測器數據"""
    print(f"\n{'='*50}")
    print(f"測試 3: 連續發送 {count} 筆感測器數據（間隔 {interval} 秒）")
    print(f"{'='*50}")
    
    import random
    
    for i in range(count):
        # 模擬溫濕度變化
        temperature = 20 + random.uniform(-2, 5)  # 18-25°C
        humidity = 50 + random.uniform(-10, 20)   # 40-70%
        
        data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "temperature": round(temperature, 1),
            "humidity": round(humidity, 1),
            "status": "正常"
        }
        
        message = json.dumps(data, ensure_ascii=False)
        result = client.publish(TOPIC_SENSOR, message, qos=1)
        
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"✅ [{i+1}/{count}] 溫度: {temperature:.1f}°C, 濕度: {humidity:.1f}%")
        else:
            print(f"❌ [{i+1}/{count}] 發布失敗")
        
        if i < count - 1:  # 最後一筆不需要等待
            time.sleep(interval)

def main():
    """主函數"""
    print("="*50)
    print("MQTT 測試發布器")
    print("="*50)
    print(f"Broker: {MQTT_BROKER}:{MQTT_PORT}")
    print(f"用戶名: {MQTT_USERNAME}")
    print("="*50)
    
    # 連接 MQTT
    print("\n正在連接 MQTT Broker...")
    client = connect_mqtt()
    
    # 顯示選單
    print("\n" + "="*50)
    print("請選擇測試項目:")
    print("1. 測試電燈狀態 (開啟)")
    print("2. 測試電燈狀態 (關閉)")
    print("3. 測試感測器數據 (單筆)")
    print("4. 連續發送感測器數據 (10筆，間隔2秒)")
    print("5. 完整測試 (所有項目)")
    print("0. 退出")
    print("="*50)
    
    while True:
        try:
            choice = input("\n請輸入選項 (0-5): ").strip()
            
            if choice == "0":
                print("\n👋 退出測試")
                break
            elif choice == "1":
                test_light_status(client, "on")
            elif choice == "2":
                test_light_status(client, "off")
            elif choice == "3":
                temp = float(input("請輸入溫度 (預設 25.5): ") or "25.5")
                hum = float(input("請輸入濕度 (預設 60.0): ") or "60.0")
                test_sensor_data(client, temp, hum)
            elif choice == "4":
                count = int(input("請輸入發送筆數 (預設 10): ") or "10")
                interval = float(input("請輸入間隔秒數 (預設 2): ") or "2")
                test_continuous_sensor_data(client, count, interval)
            elif choice == "5":
                print("\n開始完整測試...")
                test_light_status(client, "on")
                time.sleep(1)
                test_light_status(client, "off")
                time.sleep(1)
                test_sensor_data(client, 25.5, 60.0)
                time.sleep(1)
                test_continuous_sensor_data(client, 5, 1)
                print("\n✅ 完整測試完成!")
            else:
                print("❌ 無效的選項，請重新輸入")
        
        except KeyboardInterrupt:
            print("\n\n⚠️  測試被中斷")
            break
        except Exception as e:
            print(f"\n❌ 發生錯誤: {e}")
    
    # 斷開連接
    print("\n正在斷開連接...")
    client.loop_stop()
    client.disconnect()
    print("✅ 已斷開連接")

if __name__ == "__main__":
    main()

