"""
Streamlit MQTT 物聯網監控儀表板
根據 PRD.md 規格實作
"""

import streamlit as st
import paho.mqtt.client as mqtt
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import time
from datetime import datetime
import io

# 頁面配置
st.set_page_config(
    page_title="MQTT 物聯網監控儀表板",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化 Session State
if 'mqtt_client' not in st.session_state:
    st.session_state.mqtt_client = None
if 'mqtt_connected' not in st.session_state:
    st.session_state.mqtt_connected = False
if 'light_status' not in st.session_state:
    st.session_state.light_status = None
if 'light_timestamp' not in st.session_state:
    st.session_state.light_timestamp = None
if 'sensor_data' not in st.session_state:
    st.session_state.sensor_data = []
if 'messages_history' not in st.session_state:
    st.session_state.messages_history = []
if 'current_temperature' not in st.session_state:
    st.session_state.current_temperature = None
if 'current_humidity' not in st.session_state:
    st.session_state.current_humidity = None

# MQTT 回調函數
def on_connect(client, userdata, flags, rc):
    """MQTT 連接成功回調"""
    if rc == 0:
        # 注意：在回調中更新 Session State 可能不會立即反映在 UI
        # 但我們仍然更新它，並在 connect_mqtt 中檢查
        st.session_state.mqtt_connected = True
        
        # 訂閱主題
        try:
            result_light = client.subscribe("客廳/light", qos=1)
            result_sensor = client.subscribe("客廳/sensor", qos=1)
            
            # 調試：打印訂閱結果
            print(f"[MQTT] 訂閱結果 - light: {result_light}, sensor: {result_sensor}")
            
            # 記錄連接成功訊息
            msg = {
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'type': 'system',
                'message': f'✅ MQTT 連接成功並已訂閱主題: 客廳/light (rc={result_light[0]}), 客廳/sensor (rc={result_sensor[0]})'
            }
            if 'messages_history' in st.session_state:
                st.session_state.messages_history.append(msg)
        except Exception as e:
            error_msg = {
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'type': 'error',
                'message': f'❌ 訂閱主題時發生錯誤: {str(e)}'
            }
            if 'messages_history' in st.session_state:
                st.session_state.messages_history.append(error_msg)
    else:
        st.session_state.mqtt_connected = False
        error_messages = {
            1: "協議版本不正確",
            2: "客戶端 ID 無效",
            3: "伺服器不可用",
            4: "用戶名或密碼錯誤",
            5: "未授權"
        }
        error_msg = error_messages.get(rc, f"未知錯誤 ({rc})")
        msg = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'type': 'error',
            'message': f'❌ 連接失敗: {error_msg}'
        }
        if 'messages_history' in st.session_state:
            st.session_state.messages_history.append(msg)

def on_message(client, userdata, msg):
    """MQTT 訊息接收回調"""
    try:
        topic = msg.topic
        payload = msg.payload.decode('utf-8')
        
        # 調試：記錄收到的原始訊息
        print(f"[MQTT] 收到訊息 - 主題: {topic}, QoS: {msg.qos}, 內容: {payload}")
        print(f"[MQTT] 主題類型: {type(topic)}, 主題長度: {len(topic)}")
        print(f"[MQTT] 預期主題 '客廳/light': {topic == '客廳/light'}")
        print(f"[MQTT] 預期主題 '客廳/sensor': {topic == '客廳/sensor'}")
        
        data = json.loads(payload)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 儲存到歷史記錄
        history_entry = {
            'timestamp': timestamp,
            'topic': topic,
            'temperature': None,
            'humidity': None,
            'light_status': None,
            'raw_message': payload
        }
        
        # 主題匹配（精確匹配）
        if topic == "客廳/light":
            # 處理電燈狀態
            print(f"[MQTT] 處理電燈狀態訊息")
            status = data.get('status', 'unknown')
            st.session_state.light_status = status
            st.session_state.light_timestamp = data.get('timestamp', timestamp)
            history_entry['light_status'] = status
            
        elif topic == "客廳/sensor":
            # 處理感測器數據
            print(f"[MQTT] 處理感測器數據訊息")
            # 處理感測器數據
            temperature = data.get('temperature')
            humidity = data.get('humidity')
            
            if temperature is not None:
                st.session_state.current_temperature = temperature
            if humidity is not None:
                st.session_state.current_humidity = humidity
            
            # 加入感測器數據列表
            sensor_entry = {
                'timestamp': timestamp,
                'datetime': datetime.now(),
                'temperature': temperature,
                'humidity': humidity,
                'status': data.get('status', '正常')
            }
            st.session_state.sensor_data.append(sensor_entry)
            
            # 限制數據數量（最多 1000 筆）
            if len(st.session_state.sensor_data) > 1000:
                st.session_state.sensor_data.pop(0)
            
            history_entry['temperature'] = temperature
            history_entry['humidity'] = humidity
        
        st.session_state.messages_history.append(history_entry)
        
        # 限制歷史記錄數量
        if len(st.session_state.messages_history) > 1000:
            st.session_state.messages_history.pop(0)
            
    except json.JSONDecodeError as e:
        st.session_state.messages_history.append({
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'type': 'error',
            'message': f'❌ JSON 解析錯誤: {str(e)}'
        })
    except Exception as e:
        st.session_state.messages_history.append({
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'type': 'error',
            'message': f'❌ 處理訊息時發生錯誤: {str(e)}'
        })

def on_subscribe(client, userdata, mid, granted_qos):
    """訂閱成功回調"""
    print(f"[MQTT] 訂閱成功 - Message ID: {mid}, Granted QoS: {granted_qos}")

def on_disconnect(client, userdata, rc):
    """MQTT 斷開連接回調"""
    st.session_state.mqtt_connected = False
    st.session_state.messages_history.append({
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'type': 'system',
        'message': '⚠️ MQTT 連接已斷開'
    })

def connect_mqtt(broker, port, username, password):
    """連接 MQTT Broker"""
    try:
        if st.session_state.mqtt_client is not None:
            disconnect_mqtt()
        
        # 生成唯一的客戶端 ID
        import uuid
        client_id = f"streamlit_client_{uuid.uuid4().hex[:8]}"
        client = mqtt.Client(client_id=client_id)
        
        if username and password:
            client.username_pw_set(username, password)
        
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_subscribe = on_subscribe
        client.on_disconnect = on_disconnect
        
        # 連接並啟動循環
        client.connect(broker, int(port), 60)
        client.loop_start()
        
        st.session_state.mqtt_client = client
        
        # 等待連接建立（最多等待 3 秒）
        max_wait = 30  # 3 秒 = 30 * 0.1
        connected = False
        for _ in range(max_wait):
            if st.session_state.mqtt_connected:
                connected = True
                break
            time.sleep(0.1)
        
        if not connected:
            # 檢查客戶端實際連接狀態
            if hasattr(client, 'is_connected') and client.is_connected():
                st.session_state.mqtt_connected = True
                connected = True
            else:
                st.session_state.messages_history.append({
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'type': 'error',
                    'message': '❌ 連接超時，請檢查 Broker 地址和端口'
                })
                disconnect_mqtt()
                return False
        
        return True
    except ConnectionRefusedError as e:
        st.session_state.messages_history.append({
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'type': 'error',
            'message': f'❌ 連接被拒絕: 請確認 Broker 地址 ({broker}:{port}) 是否正確，以及 MQTT 服務是否運行'
        })
        return False
    except Exception as e:
        st.session_state.messages_history.append({
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'type': 'error',
            'message': f'❌ 連接失敗: {str(e)}'
        })
        return False

def disconnect_mqtt():
    """斷開 MQTT 連接"""
    if st.session_state.mqtt_client:
        try:
            st.session_state.mqtt_client.loop_stop()
            st.session_state.mqtt_client.disconnect()
            st.session_state.mqtt_client = None
            st.session_state.mqtt_connected = False
            return True
        except Exception as e:
            st.session_state.messages_history.append({
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'type': 'error',
                'message': f'❌ 斷開連接時發生錯誤: {str(e)}'
            })
            return False
    return False

def export_to_excel():
    """將歷史數據匯出為 Excel 檔案"""
    try:
        if not st.session_state.messages_history:
            return None
        
        # 準備數據
        export_data = []
        for msg in st.session_state.messages_history:
            if 'topic' in msg:  # 只匯出有主題的訊息（排除系統訊息）
                export_data.append({
                    '時間戳記': msg.get('timestamp', ''),
                    '主題': msg.get('topic', ''),
                    '溫度 (°C)': msg.get('temperature', ''),
                    '濕度 (%)': msg.get('humidity', ''),
                    '電燈狀態': msg.get('light_status', ''),
                    '原始 JSON 訊息': msg.get('raw_message', '')
                })
        
        if not export_data:
            return None
        
        # 建立 DataFrame
        df = pd.DataFrame(export_data)
        
        # 建立 Excel 檔案
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='MQTT數據')
        
        output.seek(0)
        
        # 生成檔案名稱
        filename = f"mqtt_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        return output, filename
    except Exception as e:
        st.session_state.messages_history.append({
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'type': 'error',
            'message': f'❌ 匯出 Excel 時發生錯誤: {str(e)}'
        })
        return None

# 側邊欄
with st.sidebar:
    st.title("⚙️ 設定")
    
    st.subheader("MQTT 連接設定")
    mqtt_broker = st.text_input("Broker 地址", value="192.168.0.252")
    mqtt_port = st.number_input("端口", value=1883, min_value=1, max_value=65535)
    mqtt_username = st.text_input("用戶名", value="pi")
    mqtt_password = st.text_input("密碼", type="password", value="raspberry")
    
    st.divider()
    
    # 連接控制
    col1, col2 = st.columns(2)
    with col1:
        if st.button("連接", type="primary", disabled=st.session_state.mqtt_connected):
            with st.spinner("正在連接 MQTT..."):
                if connect_mqtt(mqtt_broker, mqtt_port, mqtt_username, mqtt_password):
                    st.success("連接成功！")
                    time.sleep(0.5)  # 短暫延遲讓訊息顯示
                else:
                    st.error("連接失敗，請檢查設定和錯誤訊息")
            st.rerun()
    
    with col2:
        if st.button("斷開", disabled=not st.session_state.mqtt_connected):
            if disconnect_mqtt():
                st.success("已斷開連接")
                time.sleep(0.5)
            st.rerun()
    
    # 連接狀態
    if st.session_state.mqtt_connected:
        # 檢查實際連接狀態
        if st.session_state.mqtt_client is not None:
            try:
                # 嘗試檢查客戶端是否真的連接
                if hasattr(st.session_state.mqtt_client, '_sock') and st.session_state.mqtt_client._sock is not None:
                    st.success("🟢 已連接")
                else:
                    st.warning("🟡 連接中...")
            except:
                st.success("🟢 已連接")
        else:
            st.success("🟢 已連接")
    else:
        st.error("🔴 未連接")
        
    # 顯示連接資訊
    if st.session_state.mqtt_client is not None and st.session_state.mqtt_connected:
        st.caption(f"Broker: {mqtt_broker}:{mqtt_port}")
    
    st.divider()
    
    st.divider()
    
    # 手動刷新按鈕
    st.subheader("頁面控制")
    if st.button("🔄 手動刷新頁面"):
        st.rerun()
    
    st.divider()
    
    # Excel 匯出
    st.subheader("數據匯出")
    if st.button("匯出為 Excel", disabled=not st.session_state.messages_history):
        result = export_to_excel()
        if result:
            output, filename = result
            st.download_button(
                label="下載 Excel 檔案",
                data=output,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("沒有可匯出的數據")
    
    # 調試資訊
    if st.session_state.mqtt_connected:
        with st.expander("🔍 調試資訊"):
            st.write(f"訊息歷史記錄數量: {len(st.session_state.messages_history)}")
            st.write(f"感測器數據數量: {len(st.session_state.sensor_data)}")
            if st.session_state.mqtt_client:
                st.write(f"MQTT 客戶端: {type(st.session_state.mqtt_client).__name__}")
                try:
                    if hasattr(st.session_state.mqtt_client, '_sock'):
                        sock = st.session_state.mqtt_client._sock
                        st.write(f"Socket 狀態: {'已連接' if sock else '未連接'}")
                except:
                    pass

# 主內容區
st.title("📊 MQTT 物聯網監控儀表板")

# 連接狀態指示
if st.session_state.mqtt_connected:
    st.success("✅ MQTT 已連接 - 正在監控設備狀態")
    if st.session_state.mqtt_client is not None:
        st.caption("已訂閱主題: 客廳/light, 客廳/sensor")
else:
    st.warning("⚠️ MQTT 未連接 - 請在側邊欄設定連接")
    # 顯示最近的錯誤訊息
    if st.session_state.messages_history:
        recent_errors = [msg for msg in st.session_state.messages_history[-5:] if msg.get('type') == 'error']
        if recent_errors:
            with st.expander("查看最近錯誤訊息"):
                for error in recent_errors:
                    st.error(f"[{error.get('timestamp', '')}] {error.get('message', '')}")

st.divider()

# 設備狀態卡片
st.header("🏠 設備狀態")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("💡 電燈狀態")
    if st.session_state.light_status is not None:
        if st.session_state.light_status == "on":
            st.success("🟢 開啟")
        elif st.session_state.light_status == "off":
            st.info("⚫ 關閉")
        else:
            st.warning(f"❓ {st.session_state.light_status}")
        
        if st.session_state.light_timestamp:
            st.caption(f"最後更新: {st.session_state.light_timestamp}")
    else:
        st.info("等待數據...")

with col2:
    st.subheader("🌡️ 溫度")
    if st.session_state.current_temperature is not None:
        st.metric("溫度", f"{st.session_state.current_temperature:.1f} °C")
    else:
        st.info("等待數據...")

with col3:
    st.subheader("💧 濕度")
    if st.session_state.current_humidity is not None:
        st.metric("濕度", f"{st.session_state.current_humidity:.1f} %")
    else:
        st.info("等待數據...")

st.divider()

# 數據視覺化
st.header("📈 溫濕度趨勢圖表")

if st.session_state.sensor_data:
    # 建立 DataFrame
    df = pd.DataFrame(st.session_state.sensor_data)
    
    # 建立雙 Y 軸圖表
    fig = make_subplots(
        rows=1, cols=1,
        specs=[[{"secondary_y": True}]],
        subplot_titles=("溫濕度變化趨勢")
    )
    
    # 添加溫度線
    if 'temperature' in df.columns and df['temperature'].notna().any():
        fig.add_trace(
            go.Scatter(
                x=df['datetime'],
                y=df['temperature'],
                name='溫度 (°C)',
                line=dict(color='red', width=2),
                mode='lines+markers'
            ),
            secondary_y=False,
        )
    
    # 添加濕度線
    if 'humidity' in df.columns and df['humidity'].notna().any():
        fig.add_trace(
            go.Scatter(
                x=df['datetime'],
                y=df['humidity'],
                name='濕度 (%)',
                line=dict(color='blue', width=2),
                mode='lines+markers'
            ),
            secondary_y=True,
        )
    
    # 設定 X 軸標題
    fig.update_xaxes(title_text="時間")
    
    # 設定 Y 軸標題
    fig.update_yaxes(title_text="溫度 (°C)", secondary_y=False)
    fig.update_yaxes(title_text="濕度 (%)", secondary_y=True)
    
    # 更新佈局
    fig.update_layout(
        height=500,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 顯示數據統計
    st.subheader("📊 數據統計")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'temperature' in df.columns and df['temperature'].notna().any():
            st.metric("平均溫度", f"{df['temperature'].mean():.1f} °C")
    
    with col2:
        if 'temperature' in df.columns and df['temperature'].notna().any():
            st.metric("最高溫度", f"{df['temperature'].max():.1f} °C")
    
    with col3:
        if 'humidity' in df.columns and df['humidity'].notna().any():
            st.metric("平均濕度", f"{df['humidity'].mean():.1f} %")
    
    with col4:
        if 'humidity' in df.columns and df['humidity'].notna().any():
            st.metric("最高濕度", f"{df['humidity'].max():.1f} %")
    
else:
    st.info("📭 尚未收到感測器數據，請確認 MQTT 連接並等待數據傳輸")

st.divider()

# 訊息歷史記錄（可選顯示）
with st.expander("📋 訊息歷史記錄（最近 50 條）"):
    if st.session_state.messages_history:
        recent_messages = st.session_state.messages_history[-50:]
        for msg in reversed(recent_messages):
            if 'type' in msg:
                # 系統訊息
                st.write(f"[{msg.get('timestamp', '')}] {msg.get('message', '')}")
            else:
                # 數據訊息
                topic = msg.get('topic', '')
                timestamp = msg.get('timestamp', '')
                st.write(f"[{timestamp}] {topic}")
                if msg.get('temperature') is not None or msg.get('humidity') is not None:
                    st.json({
                        '溫度': msg.get('temperature'),
                        '濕度': msg.get('humidity')
                    })
                elif msg.get('light_status'):
                    st.json({
                        '狀態': msg.get('light_status')
                    })
    else:
        st.info("尚無訊息記錄")

# 自動刷新機制：當 MQTT 連接時，定期更新頁面以顯示新訊息
if st.session_state.mqtt_connected:
    # 初始化最後訊息計數
    if 'last_message_count' not in st.session_state:
        st.session_state.last_message_count = 0
    
    # 檢查是否有新訊息
    current_message_count = len(st.session_state.messages_history)
    if current_message_count > st.session_state.last_message_count:
        # 有新訊息，立即更新
        st.session_state.last_message_count = current_message_count
        time.sleep(0.3)  # 短暫延遲讓回調完成
        st.rerun()
    else:
        # 沒有新訊息，定期刷新（每 3 秒）以保持連接活躍
        time.sleep(3)
        st.rerun()
