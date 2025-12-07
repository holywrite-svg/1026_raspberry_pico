# Lesson 6 Flask MQTT 專案分析

## 1. 專案概述
這是一個基於 Flask 和 MQTT 的物聯網監控儀表板。它的主要功能是接收來自 MQTT Broker 的感測器數據（溫度、濕度、光照狀態），並通過網頁即時顯示這些資訊。此專案設計用來替代 Streamlit，以解決相容性問題並提供更靈活的 Web 介面。

## 2. 檔案結構分析
- **app_flask.py**: 核心後端程式。負責啟動 Flask 伺服器、管理 MQTT 連線、處理數據儲存（記憶體與 CSV）以及提供 API 介面。
- **templates/index.html**: 前端頁面。使用 HTML/CSS/JS 構建，包含 Chart.js 圖表和 Socket.IO 客戶端，負責數據的視覺化呈現。
- **sensor_data.csv**: 用於持久化存儲歷史數據的檔案。
- **PRD.md / README.md**: 專案說明文件。

## 3. 程式邏輯詳細分析

### 後端邏輯 (`app_flask.py`)
主要由三個部分組成：
1.  **Flask Web Server**:
    - 使用 `Flask` 提供網頁服務，`Flask-SocketIO` 支援即時通訊。
    - 路由 `/`: 回傳主頁面。
    - API `/api/latest`: 回傳最新的感測器數據。
    - API `/api/history`: 回傳最近由 CSV 載入或接收到的 100 筆歷史數據。

2.  **MQTT Client**:
    - 使用 `paho-mqtt` 連接 MQTT Broker (預設 `localhost:1883`)。
    - 訂閱主題 `客廳/感測器`。
    - **回調函數 (`on_message`)**:
        - 接收訊息後解析 JSON。
        - 更新全域變數 `latest_data` 與 `sensor_data`。
        - 將數據寫入 `sensor_data.csv`。
        - 透過 WebSocket (`socketio.emit`) 即時推送數據給前端。
        - 維護記憶體中的數據列表長度不超過 100 筆。

3.  **數據持久化**:
    - 啟動時從 CSV 讀取最近 100 筆數據恢復狀態。
    - 每次收到新訊息時追加寫入 CSV。

### 前端邏輯 (`templates/index.html`)
- **介面設計**: 使用 CSS Grid/Flexbox 佈局，包含狀態燈、數據卡片與歷史趨勢圖。
- **即時更新**:
    - 初始化時透過 HTTP API 獲取數據。
    - 建立 `Socket.IO` 連線監聽 `new_data` 事件，收到後立即更新介面與狀態燈。
    - 使用 `Chart.js` 繪製溫濕度折線圖。

## 4. 您可以修改的部分

### 設定與參數 (Configuration)
位於 `app_flask.py` 頂部的全域變數：
- **MQTT 設定**:
    ```python
    MQTT_BROKER = "localhost"  # 修改為您的 Broker IP (如 192.168.x.x)
    MQTT_TOPIC = "客廳/感測器"  # 修改為您感測器發送的主題
    ```
- **數據保存量**:
    在 `load_from_csv` 和 `on_message` 函數中，目前設定為 `100` 筆。您可以根據需求增加此數值。

### 擴充功能 (Features)
1.  **新增感測器數據**:
    - 如果您的硬體發送了新的數據（例如氣壓 `pressure`），您需要：
        1. 在 `on_message` 中解析該欄位。
        2. 更新 `latest_data` 字典結構。
        3. 修改 `save_to_csv` 加入新欄位（注意：這可能需要刪除舊 CSV 或處理 header 不一致的問題）。
        4. 在 `index.html` 中新增對應的顯示卡片與圖表數據集。

2.  **更換資料庫**:
    - 目前使用 CSV 儲存。若數據量大，建議將 `save_to_csv` 和 `load_from_csv` 改寫為使用 SQLite 或 MySQL，以提升效能與查詢能力。

### 介面外觀 (UI/UX)
位於 `templates/index.html`：
- **樣式 (CSS)**:
    - 可以修改 `.body` 的 `background` 改換背景顏色或圖片。
    - 修改 `.sensor-card` 的樣式來調整卡片外觀。
- **圖表 (Chart.js)**:
    - 修改 `new Chart` 中的 `borderColor` 或 `backgroundColor` 來改變線條顏色。
    - 調整 `options` 來改變圖表的互動行為或座標軸顯示。

## 5. 優化建議
- **環境變數**: 建議將 MQTT Broker IP、Port 等敏感或易變動的配置移至 `.env` 檔案管理。
- **錯誤處理**: 目前對於 JSON 解析錯誤僅做簡單列印，建議加入更詳細的錯誤日誌記錄。
- **CSV 效能**: 隨著時間推移 CSV 會越來越大，讀取全檔會變慢。建議實作 "Log Rotation" (按日期分檔) 或轉用資料庫。
