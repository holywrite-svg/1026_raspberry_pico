# 開發問題與解決方案筆記

這份文件記錄了在開發過程中遇到的問題、診斷步驟以及解決方案，涵蓋虛擬環境、編輯器延伸模組和 Git 操作等方面。

---

## 虛擬環境與專案設定

### 核心概念

- **基本原則**：永遠要在專案的根目錄下建立並啟動虛擬環境。
- **錯誤原因分析**：
  - 在此次錯誤中，問題發生於在專案的上層資料夾（包含 `.git` 的父目錄）啟動了虛擬環境。
  - 這導致虛擬環境在解析 Python 路徑時產生混淆，無法正確識別並啟用為專案設定的 Python 版本。
  - 當一個專案（子容器）內嵌在另一個 Git 倉庫（父容器）中時，可能會導致類似的環境變數或路徑衝突。
- **正確操作**：進入專案的實際工作目錄後，再啟動虛擬環境。

### 終端機無法自動進入虛擬環境

- **問題描述**：老師的電腦在執行 Python 程式碼時會自動啟用虛擬環境，但我的終端機沒有此行為。
- **解決方案**：問題在於終端機 session 沒有更新。**重新開啟一個新的終端機視窗**後，設定便正確載入，問題解決。

---

## Cursor GEMINI 延伸模組無法執行的解決方法
- 最後因為版本問題導致無法做連線
### 1. 問題診斷步驟

#### 檢查延伸模組是否已安裝
- 開啟 Cursor。
- 點擊左側擴展圖示（或按 `Ctrl+Shift+X`）。
- 搜尋 "Gemini" 或 "Google Gemini"，確認是否已安裝並啟用。

#### 檢查延伸模組狀態
- 查看延伸模組是否顯示錯誤訊息或需要重新載入。
- 開啟 Cursor 的輸出面板（`Ctrl+Shift+U`）尋找相關的錯誤訊息。

### 2. 常見解決方法

#### 方法一：檢查延伸模g組是否已啟用（最重要！）
1.  開啟 Cursor 設定（`Ctrl+,` 或 `File > Preferences > Settings`）。
2.  搜尋 `geminicodeassist.enable`。
3.  確認該選項已勾選/啟用。
4.  **重要**：變更此設定後，需要重新載入 Cursor 視窗才能生效。
5.  重新載入方法：按 `Ctrl+Shift+P`，輸入 "Reload Window" 並執行。

#### 方法二：移除重複的延伸模組版本
如果發現有多個版本的 GEMINI 延伸模組（例如 `2.56.0` 和 `2.57.0`），可能造成衝突。
- **方案 A (在 Cursor 中操作)**：點擊舊版延伸模組，選擇 "Uninstall"。
- **方案 B (手動刪除)**：
  ```bash
  # 刪除指定的舊版本目錄
  rm -rf ~/.cursor-server/extensions/google.geminicodeassist-2.56.0-universal
  ```
- 完成後重新啟動 Cursor。

#### 方法三：檢查 API 金鑰設定
- 確認已在設定中正確填寫 Google Gemini API 金鑰，且金鑰仍然有效。

#### 方法四：重新安裝延伸模組
1.  在 Cursor 中解除安裝 GEMINI 延伸模組。
2.  關閉並重新啟動 Cursor。
3.  重新安裝 "Gemini Code Assist" 延伸模組。
4.  確認安裝後，再次檢查 `geminicodeassist.enable` 是否已啟用，並重新載入視窗。

#### 方法五：檢查網路連線
- 確認網路連線正常，且防火牆或代理伺服器未阻擋 Cursor 的網路請求。
- 測試連線：
  ```bash
  curl -I https://generativelanguage.googleapis.com
  ```

#### 方法六：檢查 Cursor 版本
- 確保 Cursor 已更新至最新版本，以避免因版本過舊導致的相容性問題。

#### 方法七：清除快取並重新載入
1.  關閉 Cursor。
2.  執行以下指令清除快取（**謹慎使用**）：
    ```bash
    # 清除延伸模組快取
    rm -rf ~/.cursor-server/data/CachedExtensions
    # 清除工作區快取
    rm -rf ~/.cursor-server/data/User/workspaceStorage
    ```
3.  重新啟動 Cursor 並重新安裝延伸模組。

#### 方法八：檢查系統權限
- 確保 Cursor 程式及其設定目錄有正確的讀寫權限。

### 3. 檢查日誌檔案

日誌檔案是尋找根本原因的關鍵。
- **日誌路徑**: `~/.cursor-server/data/logs/` (尋找最新日期的目錄)
- **延伸模組日誌**: `~/.cursor-server/data/logs/[日期]/exthost*/remoteexthost.log`
- **快速檢查指令**:
  ```bash
  # 查看最新的延伸模組日誌，並過濾 gemini 或 error 相關訊息
  tail -100 ~/.cursor-server/data/logs/$(ls -t ~/.cursor-server/data/logs/ | head -1)/exthost*/remoteexthost.log | grep -i "gemini\|error"
  ```

### 4. 快速檢查指令腳本

```bash
# 檢查 Cursor 相關進程是否正在執行
ps aux | grep cursor

# 檢查 GEMINI 延伸模組是否已安裝
ls -la ~/.cursor-server/extensions/ | grep -i gemini

# 檢查是否有多个版本的延伸模組造成衝突
ls -la ~/.cursor-server/extensions/google.geminicodeassist-*

# 檢查延伸模組的啟用配置
cat ~/.cursor-server/extensions/google.geminicodeassist-*/package.json | grep -A 3 "geminicodeassist.enable"

# 查看最新的延伸模組日誌
tail -50 ~/.cursor-server/data/logs/$(ls -t ~/.cursor-server/data/logs/ | head -1)/exthost*/remoteexthost.log

# 檢查 gemini 相關進程是否正在執行
ps aux | grep gemini
```

---

## 如何同步到 GitHub

### 基本同步命令

```bash
# 將所有變更加入暫存區
git add .

# 提交變更並附上提交訊息
git commit -m "你的提交訊息"

# 推送到 GitHub 遠端倉庫的 main 分支
git push origin main
```

### 方法 1：使用 Personal Access Token (HTTPS)

1.  **生成 Token**：
   -   前往 GitHub Tokens 設定頁面。
   -   點擊 "Generate new token (classic)"。
   -   勾選 `repo` 權限範圍。
   -   複製生成好的 Token。

2.  **推送程式碼**：
   -   執行 `git push` 時，若提示輸入密碼，請貼上剛剛複製的 Token。

### 方法 2：設定 SSH 金鑰

1.  **生成 SSH 金鑰** (如果尚未設定)：
    ```bash
    ssh-keygen -t ed25519 -C "your_email@example.com"
    ```

2.  **將公鑰新增至 GitHub**：
   -   複製公鑰內容：
      ```bash
      cat ~/.ssh/id_ed25519.pub
      ```
    -   前往 GitHub SSH Keys 設定頁面。
    -   點擊 "New SSH key"，貼上公鑰內容。

3.  **更改遠端倉庫 URL 為 SSH 格式**：
    ```bash
    git remote set-url origin git@github.com:holywrite-svg/1026_raspberry_pico.git
    ```

4.  **推送程式碼**：
    ```bash
    git push -u origin main
    ```

---

## Agent 執行紀錄參考

以下紀錄展示了當 `gh` (GitHub CLI) 指令不存在時，系統自動切換回使用 `git clone` 的備用方案。這是一個很好的容錯設計範例。

```log
正在克隆 roberthsu2003/learningPythonFromZero 倉庫。
--: 列 1: gh：指令找不到
未安裝 GitHub CLI (gh)。改用 git clone 克隆該倉庫：
正複製到 'learningPythonFromZero'...
已成功克隆倉庫。確認內容：
總用量 96
drwxrwxr-x 19 pi pi 4096 11月  9 10:41 .
drwxrwxr-x  5 pi pi 4096 11月  9 10:41 ..
drwxrwxr-x  3 pi pi 4096 11月  9 10:41 BeautifulSoup4的基本操作
... (省略部分檔案列表) ...
-rw-rw-r--  1 pi pi    8 11月  9 10:41 requirements.txt
drwxrwxr-x  3 pi pi 4096 11月  9 10:41 下載youbike即時資訊
已成功克隆 learningPythonFromZero 倉庫到 /home/pi/Documents/Github/learningPythonFromZero/。

備註： 系統未安裝 GitHub CLI (gh)，已改用 git clone 完成克隆。
如需安裝 GitHub CLI，可執行：
sudo apt update && sudo apt install gh
```


