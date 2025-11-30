# MQTT Broker 設定說明

## 📋 目錄
1. [問題診斷](#問題診斷)
2. [解決方案](#解決方案)
3. [故障排除](#故障排除)
4. [測試連接](#測試連接)
5. [安全建議](#安全建議)
6. [常見問題](#常見問題)

---

## 🔍 問題診斷

### 常見錯誤訊息

如果 Pico 無法連接到 MQTT Broker，可能會出現以下錯誤：

| 錯誤訊息 | 可能原因 | 解決方法 |
|---------|---------|---------|
| `ECONNABORTED` | 連接被中止，通常是 Mosquitto 只監聽 localhost | 修改設定讓 Mosquitto 監聽所有介面 |
| `EHOSTUNREACH` | 無法到達主機，IP 位址錯誤或網路不通 | 檢查 IP 位址和網路連接 |
| `Connection refused` | 連接被拒絕，服務未運行或防火牆阻擋 | 檢查服務狀態和防火牆設定 |
| `[Errno 113] EHOSTUNREACH` | 使用 `localhost` 在 Pico 上（Pico 的 localhost 不是 Raspberry Pi） | 使用 Raspberry Pi 的實際 IP 位址 |

### 核心問題

**主要問題**：Mosquitto 預設只監聽 `127.0.0.1:1883`（localhost），這意味著：
- ✅ Raspberry Pi 本機可以連接（使用 `localhost` 或 `127.0.0.1`）
- ❌ 外部設備（如 Pico、其他電腦）無法連接

**解決方法**：讓 Mosquitto 監聽所有網路介面（`0.0.0.0:1883`）

## 🔧 解決方案

### 步驟 1: 檢查 Mosquitto 監聽狀態

在 Raspberry Pi 上執行：
```bash
sudo netstat -tlnp | grep 1883
```

或者使用 `ss` 命令：
```bash
sudo ss -tlnp | grep 1883
```

**判斷結果**：
- ❌ `127.0.0.1:1883` → 只監聽 localhost，**需要修改**
- ✅ `0.0.0.0:1883` 或 `:::1883` → 監聽所有介面，**設定正確**

如果看到 `127.0.0.1:1883`，表示只監聽 localhost，需要修改設定。

### 步驟 2: 備份現有設定檔（建議）

```bash
sudo cp /etc/mosquitto/mosquitto.conf /etc/mosquitto/mosquitto.conf.backup
```

### 步驟 3: 編輯 Mosquitto 設定檔

```bash
sudo nano /etc/mosquitto/mosquitto.conf
```

### 步驟 4: 確保有以下設定

在設定檔的**最後**加入或確認以下內容：

```conf
# 監聽所有網路介面（不只是 localhost）
# 這行很重要！讓外部設備可以連接
listener 1883 0.0.0.0

# 如果需要認證（推薦）
allow_anonymous false
password_file /etc/mosquitto/passwd
```

**重要說明**：
- `listener 1883 0.0.0.0` → 讓 Mosquitto 監聽所有網路介面（IPv4）
- `listener 1883` → 如果只寫這行，預設也是監聽所有介面
- 如果沒有 `listener` 設定，預設只監聽 localhost
- `0.0.0.0` 表示監聽所有 IPv4 介面
- `::` 表示監聽所有 IPv6 介面

**注意**：如果設定檔中已經有 `bind_address` 設定，請註解掉或刪除它：
```conf
# bind_address 127.0.0.1  # 註解掉這行
```

### 步驟 5: 檢查設定檔語法

在重啟前，先檢查設定檔是否有語法錯誤：
```bash
sudo mosquitto -c /etc/mosquitto/mosquitto.conf -t
```

如果沒有錯誤，會顯示 `Configuration loaded.`

### 步驟 6: 重啟 Mosquitto

```bash
sudo systemctl restart mosquitto
```

檢查服務狀態：
```bash
sudo systemctl status mosquitto
```

應該看到 `Active: active (running)`

### 步驟 7: 確認設定生效

再次檢查監聽狀態：
```bash
sudo netstat -tlnp | grep 1883
```

**預期結果**：
- ✅ `0.0.0.0:1883` → IPv4 監聽所有介面
- ✅ `:::1883` → IPv6 監聽所有介面
- ❌ `127.0.0.1:1883` → 如果還是這個，設定沒有生效

如果還是看到 `127.0.0.1:1883`，請檢查：
1. 設定檔是否正確儲存
2. 是否有其他設定檔覆蓋了設定（檢查 `/etc/mosquitto/conf.d/` 目錄）
3. 查看 Mosquitto 日誌：`sudo journalctl -u mosquitto -n 50`

### 步驟 8: 檢查防火牆（如果需要）

如果還是無法連接，檢查防火牆設定：

**檢查 UFW 防火牆狀態**：
```bash
sudo ufw status
```

**如果需要開放 1883 埠**：
```bash
sudo ufw allow 1883/tcp
sudo ufw reload
```

**檢查 iptables（如果使用）**：
```bash
sudo iptables -L -n | grep 1883
```

**暫時關閉防火牆測試**（僅用於測試，不建議在生產環境）：
```bash
sudo ufw disable  # 關閉
# 測試後記得重新開啟
sudo ufw enable   # 開啟
```

## 🧪 測試連接

### 方法 1: 在 Raspberry Pi 上測試（使用 IP 位址）

**步驟 1：取得 Raspberry Pi 的 IP 位址**
```bash
hostname -I
# 或
ip addr show wlan0 | grep "inet " | awk '{print $2}' | cut -d/ -f1
```

**步驟 2：開啟兩個終端機視窗**

**終端機 1 - 訂閱測試**：
```bash
mosquitto_sub -h 192.168.137.113 -t "test" -u "pi" -P "raspberry" -v
```
（將 `192.168.137.113` 替換為您的實際 IP）

**終端機 2 - 發布測試**：
```bash
mosquitto_pub -h 192.168.137.113 -t "test" -m "Hello MQTT" -u "pi" -P "raspberry"
```

如果訂閱端收到訊息，表示設定成功！

### 方法 2: 使用 localhost 測試（僅在 Raspberry Pi 上）

```bash
# 訂閱
mosquitto_sub -h localhost -t "test" -u "pi" -P "raspberry" -v

# 發布（另一個終端）
mosquitto_pub -h localhost -t "test" -m "Hello" -u "pi" -P "raspberry"
```

### 方法 3: 從 Pico 測試

在 Pico 上執行程式後，從 Raspberry Pi 發布訊息：
```bash
mosquitto_pub -h 192.168.137.113 -t "客廳/message" -m "測試訊息" -u "pi" -P "raspberry"
```

如果 Pico 的 LED 亮起，表示連接成功！

## 🔒 安全建議

### 1. 使用密碼認證

**不要使用匿名連接**：
```conf
allow_anonymous false
password_file /etc/mosquitto/passwd
```

**建立使用者密碼檔**：
```bash
# 建立密碼檔並新增使用者
sudo mosquitto_passwd -c /etc/mosquitto/passwd pi

# 新增更多使用者（不需要 -c 參數）
sudo mosquitto_passwd /etc/mosquitto/passwd another_user
```

### 2. 使用 TLS/SSL（生產環境推薦）

在生產環境中，建議使用加密連接：
```conf
listener 8883
cafile /etc/mosquitto/certs/ca.crt
certfile /etc/mosquitto/certs/server.crt
keyfile /etc/mosquitto/certs/server.key
```

### 3. 限制訪問

**使用防火牆限制可連接的 IP**：
```bash
# 只允許特定 IP 連接
sudo ufw allow from 192.168.1.0/24 to any port 1883
```

**在 Mosquitto 設定中限制**：
```conf
# 只允許特定 IP 範圍
acl_file /etc/mosquitto/acl
```

### 4. 定期更新

保持 Mosquitto 和系統更新：
```bash
sudo apt update
sudo apt upgrade mosquitto
```

---

## ❓ 常見問題

### Q1: 修改設定後還是無法連接？

**檢查清單**：
1. ✅ 確認設定檔已正確儲存
2. ✅ 確認已重啟 Mosquitto 服務
3. ✅ 確認監聽狀態是 `0.0.0.0:1883`
4. ✅ 檢查防火牆是否開放 1883 埠
5. ✅ 確認 Pico 和 Raspberry Pi 在同一個 WiFi 網路
6. ✅ 確認 IP 位址正確（不是 `localhost`）

**查看日誌**：
```bash
sudo journalctl -u mosquitto -f
```

### Q2: Pico 顯示 `EHOSTUNREACH` 錯誤？

**原因**：使用了 `localhost` 或 IP 位址錯誤

**解決方法**：
- ❌ 不要使用 `localhost`（在 Pico 上 `localhost` 是 Pico 自己）
- ✅ 使用 Raspberry Pi 的實際 IP 位址（例如 `192.168.137.113`）

**取得 IP 位址**：
```bash
hostname -I
```

### Q3: 連接成功但收不到訊息？

**檢查**：
1. 確認訂閱的主題名稱正確
2. 確認發布的主題名稱與訂閱的一致
3. 檢查 QoS 等級設定
4. 確認認證資訊正確

### Q4: 如何查看 Mosquitto 的完整設定？

```bash
sudo mosquitto -c /etc/mosquitto/mosquitto.conf -v
```

### Q5: 如何重置 Mosquitto 設定？

```bash
# 還原備份
sudo cp /etc/mosquitto/mosquitto.conf.backup /etc/mosquitto/mosquitto.conf
sudo systemctl restart mosquitto
```

### Q6: 多個設定檔的優先順序？

Mosquitto 會讀取：
1. `/etc/mosquitto/mosquitto.conf`（主設定檔）
2. `/etc/mosquitto/conf.d/*.conf`（額外設定檔，按字母順序）

後面的設定會覆蓋前面的設定。

---

## 📝 快速參考

### 完整設定檔範例

```conf
# /etc/mosquitto/mosquitto.conf

# 監聽所有網路介面
listener 1883 0.0.0.0

# 認證設定
allow_anonymous false
password_file /etc/mosquitto/passwd

# 日誌設定
log_dest file /var/log/mosquitto/mosquitto.log
log_type error
log_type warning
log_type notice
log_type information

# 連線設定
max_connections -1
max_inflight_messages 20
max_queued_messages 1000
```

### 常用指令

```bash
# 檢查服務狀態
sudo systemctl status mosquitto

# 啟動服務
sudo systemctl start mosquitto

# 停止服務
sudo systemctl stop mosquitto

# 重啟服務
sudo systemctl restart mosquitto

# 查看日誌
sudo journalctl -u mosquitto -f

# 檢查監聽狀態
sudo netstat -tlnp | grep 1883
```

---

## 📚 相關資源

- [Mosquitto 官方文件](https://mosquitto.org/documentation/)
- [MQTT 協議說明](http://mqtt.org/)
- [Pico W WiFi 文件](https://datasheets.raspberrypi.com/picow/connecting-to-the-internet-with-pico-w.pdf)

---

**最後更新**：2025-11-30

