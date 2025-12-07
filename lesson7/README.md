# Lesson 7: Raspberry Pi Pico W Wi-Fi 連線教學

這是一個專為 **Raspberry Pi Pico W** (MicroPython) 設計的 Wi-Fi 連線基礎範例。包含了一個封裝好的連線模組以及主執行程式。

## 檔案說明

### 1. `wifi_connect.py` (Wi-Fi 連線模組)
這是一個工具模組，負責處理底層的網路連線邏輯，讓主程式更簡潔。

**主要變數與功能：**
*   **設定區塊**: 檔案開頭定義了 `WIFI_SSID` 和 `WIFI_PASSWORD`，請在此填入您的 WiFi 帳號密碼。
*   **`connect(ssid, password, retry)`**: 
    *   初始化 WLAN 介面 (`network.STA_IF`) 並啟動 (`active(True)`)。
    *   嘗試連線至指定的 WiFi AP。
    *   **重試機制**: 透過迴圈 (預設 20 次) 檢查連線狀態，每次間隔 1 秒，避免程式在連線過程中卡住。
    *   **回傳**: 連線成功回傳 WLAN 物件；若超過重試次數仍失敗，則拋出 `RuntimeError`。
*   **`disconnect()`**: 斷開連線並關閉 WLAN 介面，釋放資源。
*   **`is_connected()`**: 回傳布林值 (`True`/`False`)，檢查目前連線狀態。
*   **`get_ip()`**: 取得並回傳目前的 IP 位址 (字串格式)。
*   **`test_internet()`**: 
    *   透過建立一個 Socket 連線至 Google DNS (8.8.8.8 port 53) 來測試。
    *   這比單純檢查 WiFi 連結更準確，能確認是否真的可以存取網際網路 (Internet)。

### 2. `main.py` (主程式)
這是程式的執行入口。

**程式邏輯：**
1.  **匯入模組**: `import wifi_connect`。
2.  **執行連線**: 呼叫 `wifi_connect.connect()`。這會依照模組內的設定進行連線，並在 Console 印出進度。
3.  **顯示資訊**: 連線成功後，呼叫 `wifi_connect.get_ip()` 顯示獲取到的 IP 位址。
4.  **網路測試**: 呼叫 `wifi_connect.test_internet()` 檢查是否能連上外網，這對於確認 Pico W 是否能進行後續的 IoT 傳輸 (如 MQTT) 非常重要。

## 使用方式
1. 打開 `wifi_connect.py`，修改 `WIFI_SSID` 和 `WIFI_PASSWORD` 為您環境的設定。
2. 將 `wifi_connect.py` 和 `main.py` 都上傳至 Raspberry Pi Pico W。
3. 在 Thonny IDE 中執行 `main.py` (或將其設為開機執行)。
