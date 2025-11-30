# Streamlit 使用指南

## 什麼是 Streamlit？

Streamlit 是一個開源的 Python 框架，用於快速建立和分享數據應用程式。它讓您可以用純 Python 程式碼建立互動式的網頁應用程式，無需前端開發經驗。

## 安裝方法

### 使用 UV（推薦）

本專案使用 `uv` 作為套件管理工具：

```bash
# 安裝 streamlit
uv pip install streamlit

# 同步專案依賴
uv sync
```

### 使用 pip（一般方法）

```bash
pip install streamlit
```

## 執行 Streamlit 應用程式

### 基本執行方式

```bash
# 使用 uv 執行
uv run streamlit run app.py

# 或直接使用 streamlit 命令
streamlit run app.py
```

### 執行選項

```bash
# 指定端口
streamlit run app.py --server.port 8502

# 指定主機地址
streamlit run app.py --server.address 0.0.0.0

# 不自動開啟瀏覽器
streamlit run app.py --server.headless true
```

## 基本語法

### 1. 標題和文字

```python
import streamlit as st

st.title("主標題")
st.header("次標題")
st.subheader("小標題")
st.write("一般文字內容")
st.markdown("**粗體文字** 或 *斜體文字*")
```

### 2. 顯示數據

```python
# 顯示 DataFrame
import pandas as pd
df = pd.DataFrame({'欄位1': [1, 2, 3], '欄位2': [4, 5, 6]})
st.dataframe(df)

# 顯示表格（靜態）
st.table(df)

# 顯示 JSON
st.json({'key': 'value'})

# 顯示程式碼
st.code("print('Hello World')", language='python')
```

### 3. 輸入元件

```python
# 文字輸入
name = st.text_input("請輸入您的姓名")

# 數字輸入
age = st.number_input("請輸入年齡", min_value=0, max_value=120)

# 滑桿
value = st.slider("選擇數值", 0, 100, 50)

# 選擇框
option = st.selectbox("選擇選項", ["選項1", "選項2", "選項3"])

# 多選
options = st.multiselect("選擇多個選項", ["A", "B", "C", "D"])

# 核取方塊
agree = st.checkbox("我同意")

# 單選按鈕
choice = st.radio("選擇一個", ["選項1", "選項2"])

# 文字區域
text = st.text_area("輸入多行文字")
```

### 4. 按鈕和互動

```python
# 按鈕
if st.button("點擊我"):
    st.write("按鈕被點擊了！")

# 下載按鈕
st.download_button(
    label="下載資料",
    data="要下載的內容",
    file_name="data.txt",
    mime="text/plain"
)
```

### 5. 檔案上傳

```python
uploaded_file = st.file_uploader("選擇檔案", type=['csv', 'txt', 'png', 'jpg'])

if uploaded_file is not None:
    # 讀取上傳的檔案
    st.write("檔案已上傳：", uploaded_file.name)
```

### 6. 圖表和視覺化

#### Streamlit 內建圖表

```python
import pandas as pd
import numpy as np

# 線圖
data = pd.DataFrame(np.random.randn(20, 3), columns=['A', 'B', 'C'])
st.line_chart(data)

# 長條圖
st.bar_chart(data)

# 區域圖
st.area_chart(data)

# 地圖（需要 lat 和 lon 欄位）
map_data = pd.DataFrame({
    'lat': [25.0330, 25.0331, 25.0332],
    'lon': [121.5654, 121.5655, 121.5656]
})
st.map(map_data)
```

#### Matplotlib

```python
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()
x = np.linspace(0, 10, 100)
y = np.sin(x)
ax.plot(x, y)
ax.set_xlabel('X 軸')
ax.set_ylabel('Y 軸')
ax.set_title('正弦波')
st.pyplot(fig)
```

#### Plotly（互動式圖表）

```python
import plotly.express as px
import plotly.graph_objects as go

# 使用 Plotly Express
df = pd.DataFrame({
    'x': np.random.randn(100),
    'y': np.random.randn(100),
    'category': np.random.choice(['A', 'B', 'C'], 100)
})

fig = px.scatter(df, x='x', y='y', color='category', 
                 title='互動式散點圖')
st.plotly_chart(fig, use_container_width=True)

# 使用 Plotly Graph Objects（更多控制）
fig = go.Figure()
fig.add_trace(go.Scatter(x=[1, 2, 3, 4], y=[10, 11, 12, 13],
                        mode='lines+markers', name='線圖'))
fig.update_layout(title='自訂 Plotly 圖表')
st.plotly_chart(fig)
```

#### Altair（聲明式圖表）

```python
import altair as alt

chart = alt.Chart(df).mark_circle().encode(
    x='x',
    y='y',
    color='category',
    size='y'
).interactive()

st.altair_chart(chart, use_container_width=True)
```

#### Bokeh

```python
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource

p = figure(title="Bokeh 圖表", x_axis_label='X', y_axis_label='Y')
p.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], legend_label="線", line_width=2)
st.bokeh_chart(p, use_container_width=True)
```

#### 圖表相關連結和資源

- **Plotly**: [plotly.com/python](https://plotly.com/python/) - 強大的互動式圖表庫
- **Altair**: [altair-viz.github.io](https://altair-viz.github.io/) - 聲明式統計視覺化
- **Matplotlib**: [matplotlib.org](https://matplotlib.org/) - Python 最流行的繪圖庫
- **Seaborn**: [seaborn.pydata.org](https://seaborn.pydata.org/) - 基於 Matplotlib 的統計視覺化
- **Bokeh**: [bokeh.org](https://bokeh.org/) - 互動式視覺化庫
- **PyDeck**: [deckgl.readthedocs.io](https://deckgl.readthedocs.io/) - 3D 地圖視覺化（Streamlit 內建支援）

### 7. 進度條和狀態

```python
# 進度條
import time
progress_bar = st.progress(0)
for i in range(100):
    time.sleep(0.01)
    progress_bar.progress(i + 1)

# 狀態訊息
st.success("成功訊息")
st.error("錯誤訊息")
st.warning("警告訊息")
st.info("資訊訊息")

# Spinner（載入動畫）
with st.spinner("處理中..."):
    time.sleep(2)
st.success("完成！")
```

### 8. 側邊欄

```python
# 在側邊欄加入元件
st.sidebar.title("側邊欄標題")
st.sidebar.selectbox("選擇", ["選項1", "選項2"])

# 或使用 with 語法
with st.sidebar:
    st.title("側邊欄")
    st.button("按鈕")
```

### 9. 分欄和容器

```python
# 分欄
col1, col2, col3 = st.columns(3)
with col1:
    st.write("第一欄")
with col2:
    st.write("第二欄")
with col3:
    st.write("第三欄")

# 容器
with st.container():
    st.write("容器內容")
    st.button("容器內的按鈕")
```

### 10. 快取功能

```python
@st.cache_data
def expensive_computation():
    # 耗時的計算
    return result

# 使用快取
result = expensive_computation()
```

## 完整範例

```python
import streamlit as st
import pandas as pd
import numpy as np

st.title("我的第一個 Streamlit 應用程式")

# 側邊欄
st.sidebar.header("設定")
num_points = st.sidebar.slider("資料點數量", 10, 100, 50)

# 主內容
st.header("資料視覺化")

# 產生資料
data = pd.DataFrame({
    'x': np.random.randn(num_points),
    'y': np.random.randn(num_points)
})

# 顯示圖表
st.line_chart(data)

# 顯示原始資料
if st.checkbox("顯示原始資料"):
    st.dataframe(data)
```

## 常用配置

### 設定頁面配置

在檔案開頭加入：

```python
st.set_page_config(
    page_title="我的應用程式",
    page_icon=":rocket:",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

### 隱藏 Streamlit 預設元素

在專案根目錄建立 `.streamlit/config.toml`：

```toml
[theme]
primaryColor="#FF6B6B"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#F0F2F6"
textColor="#262730"
font="sans serif"

[browser]
gatherUsageStats = false
```

## 部署應用程式

### Streamlit Cloud

1. 將程式碼推送到 GitHub
2. 前往 [streamlit.io/cloud](https://streamlit.io/cloud)
3. 連接 GitHub 帳號並選擇專案
4. 部署完成！

### 其他部署方式

- **Docker**：使用 Streamlit 官方 Docker 映像
- **Heroku**：使用 Procfile 部署
- **AWS/GCP/Azure**：使用雲端服務部署

## 資訊互動

### 即時更新和動態內容

```python
import streamlit as st
import time
import random

# 自動重新整理
placeholder = st.empty()
for seconds in range(10):
    placeholder.write(f"⏰ {seconds} 秒")
    time.sleep(1)
placeholder.write("✅ 完成！")
```

### 多步驟表單和對話流程

```python
# 使用 Session State 管理多步驟流程
if 'step' not in st.session_state:
    st.session_state.step = 1

if st.session_state.step == 1:
    st.write("步驟 1: 輸入基本資訊")
    name = st.text_input("姓名")
    if st.button("下一步"):
        st.session_state.name = name
        st.session_state.step = 2
        st.rerun()

elif st.session_state.step == 2:
    st.write(f"您好，{st.session_state.name}！")
    st.write("步驟 2: 確認資訊")
    if st.button("返回"):
        st.session_state.step = 1
        st.rerun()
```

### 即時數據流和 WebSocket 整合

```python
# 模擬即時數據流
import pandas as pd
import numpy as np

chart_placeholder = st.empty()

for i in range(100):
    # 產生新數據
    data = pd.DataFrame({
        'time': range(i, i+10),
        'value': np.random.randn(10).cumsum()
    })
    
    # 更新圖表
    chart_placeholder.line_chart(data)
    time.sleep(0.1)
```

### 使用者輸入驗證和回饋

```python
# 表單驗證
with st.form("驗證表單"):
    email = st.text_input("電子郵件")
    password = st.text_input("密碼", type="password")
    submitted = st.form_submit_button("登入")
    
    if submitted:
        if "@" not in email:
            st.error("請輸入有效的電子郵件地址")
        elif len(password) < 6:
            st.warning("密碼長度至少需要 6 個字元")
        else:
            st.success("登入成功！")
```

### 互動式篩選和查詢

```python
import pandas as pd

# 載入資料
df = pd.DataFrame({
    '產品': ['A', 'B', 'C', 'D', 'E'] * 20,
    '價格': np.random.randint(10, 100, 100),
    '類別': np.random.choice(['電子', '服飾', '食品'], 100)
})

# 互動式篩選
category_filter = st.multiselect("選擇類別", df['類別'].unique())
price_range = st.slider("價格範圍", 
                        int(df['價格'].min()), 
                        int(df['價格'].max()),
                        (int(df['價格'].min()), int(df['價格'].max())))

# 應用篩選
filtered_df = df[
    (df['類別'].isin(category_filter) if category_filter else True) &
    (df['價格'] >= price_range[0]) &
    (df['價格'] <= price_range[1])
]

st.dataframe(filtered_df)
st.write(f"找到 {len(filtered_df)} 筆資料")
```

### 聊天機器人和對話介面

```python
# 簡單的聊天介面
if 'messages' not in st.session_state:
    st.session_state.messages = []

# 顯示歷史訊息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 使用者輸入
if prompt := st.chat_input("輸入訊息..."):
    # 加入使用者訊息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # 模擬回應
    response = f"您說：{prompt}"
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)
```

## 安全性

### 敏感資訊保護

```python
import streamlit as st
import os

# 使用環境變數儲存敏感資訊
api_key = os.getenv("API_KEY")
if not api_key:
    st.error("請設定 API_KEY 環境變數")

# 使用 secrets.toml（僅限 Streamlit Cloud）
# 在 .streamlit/secrets.toml 中儲存：
# [secrets]
# api_key = "your-secret-key"

try:
    api_key = st.secrets["api_key"]
except:
    st.warning("無法讀取 secrets")
```

### 檔案上傳安全性

```python
import streamlit as st
import hashlib

uploaded_file = st.file_uploader("上傳檔案", type=['csv', 'txt'])

if uploaded_file is not None:
    # 檢查檔案大小（限制為 10MB）
    if uploaded_file.size > 10 * 1024 * 1024:
        st.error("檔案大小超過 10MB 限制")
    else:
        # 檢查檔案類型
        file_extension = uploaded_file.name.split('.')[-1]
        if file_extension not in ['csv', 'txt']:
            st.error("不支援的檔案類型")
        else:
            # 計算檔案雜湊值
            file_hash = hashlib.md5(uploaded_file.read()).hexdigest()
            st.write(f"檔案雜湊值：{file_hash}")
            uploaded_file.seek(0)  # 重置檔案指標
```

### 使用者認證

```python
import streamlit as st
import hashlib

# 簡單的密碼驗證（生產環境應使用更安全的方法）
def check_password():
    """回傳 True 如果使用者輸入正確密碼"""
    def password_entered():
        if st.session_state["password"] == "mypassword":  # 實際應使用環境變數
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("輸入密碼", type="password", 
                     on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("輸入密碼", type="password", 
                     on_change=password_entered, key="password")
        st.error("密碼錯誤")
        return False
    else:
        return True

if check_password():
    st.write("歡迎！您已成功登入")
```

### SQL 注入防護

```python
import streamlit as st
import sqlite3

# 使用參數化查詢（防止 SQL 注入）
def safe_query(user_input):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # ✅ 正確：使用參數化查詢
    cursor.execute("SELECT * FROM users WHERE name = ?", (user_input,))
    
    # ❌ 錯誤：直接字串拼接（容易受到 SQL 注入攻擊）
    # cursor.execute(f"SELECT * FROM users WHERE name = '{user_input}'")
    
    results = cursor.fetchall()
    conn.close()
    return results
```

### XSS（跨站腳本攻擊）防護

```python
import streamlit as st
import html

# Streamlit 自動轉義 HTML，但使用 markdown 時需注意
user_input = st.text_input("輸入內容")

# ✅ 安全：Streamlit 會自動轉義
st.write(user_input)

# ⚠️ 注意：使用 markdown 時要小心
# 如果必須顯示使用者輸入的 HTML，先進行轉義
safe_input = html.escape(user_input)
st.markdown(safe_input)
```

### HTTPS 和部署安全

```python
# 在 .streamlit/config.toml 中設定
# [server]
# enableCORS = false
# enableXsrfProtection = true
# maxUploadSize = 200
# maxMessageSize = 200

# 生產環境建議：
# 1. 使用 HTTPS
# 2. 設定適當的 CORS 政策
# 3. 限制檔案上傳大小
# 4. 使用環境變數管理敏感資訊
# 5. 定期更新 Streamlit 版本
```

### 最佳安全實踐

1. **永遠不要**在程式碼中硬編碼密碼或 API 金鑰
2. **使用**環境變數或 `secrets.toml` 儲存敏感資訊
3. **驗證**所有使用者輸入
4. **限制**檔案上傳大小和類型
5. **使用**參數化查詢防止 SQL 注入
6. **定期更新** Streamlit 和依賴套件
7. **在生產環境**使用 HTTPS
8. **實作**適當的存取控制機制

## 實用技巧

1. **使用 Session State 儲存狀態**
   ```python
   if 'counter' not in st.session_state:
       st.session_state.counter = 0
   
   if st.button("增加"):
       st.session_state.counter += 1
   
   st.write("計數器：", st.session_state.counter)
   ```

2. **條件式顯示**
   ```python
   if st.checkbox("顯示內容"):
       st.write("這是條件式顯示的內容")
   ```

3. **表單**
   ```python
   with st.form("我的表單"):
       name = st.text_input("姓名")
       submitted = st.form_submit_button("提交")
       if submitted:
           st.write(f"您好，{name}！")
   ```

## 進階使用

### 多頁面應用程式

建立 `pages/` 目錄結構：

```
app.py
pages/
  ├── page1.py
  ├── page2.py
  └── page3.py
```

```python
# app.py（主頁面）
import streamlit as st

st.title("主應用程式")
st.write("這是主頁面")

# pages/page1.py
import streamlit as st
st.title("頁面 1")
st.write("這是第一個子頁面")

# pages/page2.py
import streamlit as st
st.title("頁面 2")
st.write("這是第二個子頁面")
```

Streamlit 會自動偵測 `pages/` 目錄並建立多頁面導航。

### 自訂主題和 CSS

```python
import streamlit as st

# 使用自訂 CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
    }
    h1 {
        color: #FF6B6B;
    }
</style>
""", unsafe_allow_html=True)

st.title("自訂樣式的頁面")
st.button("自訂按鈕")
```

### 效能優化

```python
import streamlit as st
import pandas as pd

# 使用 @st.cache_data 快取資料
@st.cache_data
def load_data():
    # 模擬載入大型資料集
    return pd.read_csv('large_file.csv')

# 使用 @st.cache_resource 快取資源（如模型）
@st.cache_resource
def load_model():
    # 載入機器學習模型
    return your_model

# 使用 TTL（Time To Live）設定快取過期時間
@st.cache_data(ttl=3600)  # 1 小時後過期
def fetch_api_data():
    return api_call()

# 使用 show_spinner 控制載入動畫
with st.spinner("載入資料中..."):
    data = load_data()
```

### 自訂元件（Custom Components）

```python
import streamlit as st
import streamlit.components.v1 as components

# 嵌入 HTML/JavaScript
components.html("""
    <div style="background-color: #f0f0f0; padding: 20px; border-radius: 10px;">
        <h2>自訂 HTML 內容</h2>
        <p>這是一個自訂的 HTML 元件</p>
    </div>
""", height=200)

# 嵌入 iframe
components.iframe("https://www.example.com", height=600)

# 使用第三方 Streamlit 元件
# 安裝：pip install streamlit-option-menu
# from streamlit_option_menu import option_menu
```

### 資料庫整合

```python
import streamlit as st
import sqlite3
import pandas as pd

# 連接資料庫
@st.cache_resource
def init_connection():
    return sqlite3.connect("database.db")

conn = init_connection()

# 查詢資料
@st.cache_data(ttl=600)
def load_data(query):
    return pd.read_sql_query(query, conn)

# 使用
data = load_data("SELECT * FROM users")
st.dataframe(data)
```

### 非同步操作

```python
import streamlit as st
import asyncio
import aiohttp

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# 在 Streamlit 中執行非同步函數
if st.button("取得資料"):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    data = loop.run_until_complete(fetch_data("https://api.example.com/data"))
    st.json(data)
```

### 狀態管理和全域變數

```python
import streamlit as st

# 初始化全域狀態
if 'global_data' not in st.session_state:
    st.session_state.global_data = {}

# 跨頁面共享資料
def set_global_data(key, value):
    st.session_state.global_data[key] = value

def get_global_data(key):
    return st.session_state.global_data.get(key)

# 使用
set_global_data('user_name', 'John')
st.write(get_global_data('user_name'))
```

### 錯誤處理和日誌

```python
import streamlit as st
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # 可能出錯的操作
    result = risky_operation()
    st.success("操作成功")
except Exception as e:
    logger.error(f"錯誤發生：{str(e)}")
    st.error(f"發生錯誤：{str(e)}")
    st.exception(e)  # 顯示完整錯誤堆疊
```

### 測試 Streamlit 應用程式

```python
# test_app.py
import streamlit as st
from streamlit.testing.v1 import AppTest

def test_app():
    at = AppTest.from_file("app.py")
    at.run()
    
    # 測試輸入
    at.text_input("name").input("John").run()
    
    # 測試按鈕點擊
    at.button("submit").click().run()
    
    # 檢查輸出
    assert "John" in at.get("markdown")[0].value
```

### 部署最佳實踐

1. **使用 requirements.txt** 明確列出所有依賴
2. **設定環境變數** 用於配置
3. **使用 secrets.toml** 儲存敏感資訊（Streamlit Cloud）
4. **優化效能** 使用快取減少計算
5. **錯誤處理** 優雅地處理異常
6. **日誌記錄** 追蹤應用程式行為
7. **版本控制** 使用 Git 管理程式碼

### 進階範例：完整的資料分析應用

```python
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="資料分析儀表板", layout="wide")

# 側邊欄
st.sidebar.header("設定")
uploaded_file = st.sidebar.file_uploader("上傳 CSV 檔案", type=['csv'])

if uploaded_file is not None:
    # 載入資料
    @st.cache_data
    def load_data(file):
        return pd.read_csv(file)
    
    df = load_data(uploaded_file)
    
    # 主內容區域
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("總記錄數", len(df))
    with col2:
        st.metric("欄位數", len(df.columns))
    with col3:
        st.metric("缺失值", df.isnull().sum().sum())
    with col4:
        st.metric("重複記錄", df.duplicated().sum())
    
    # 圖表
    col1, col2 = st.columns(2)
    
    with col1:
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        if len(numeric_cols) > 0:
            selected_col = st.selectbox("選擇數值欄位", numeric_cols)
            fig = px.histogram(df, x=selected_col, title=f"{selected_col} 分佈")
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.dataframe(df.describe())
    
    # 資料表格
    st.subheader("原始資料")
    st.dataframe(df, use_container_width=True)
```

## MQTT 物聯網整合

Streamlit 可以與 MQTT（Message Queuing Telemetry Transport）協議整合，實現與物聯網設備的即時通訊。MQTT 是一種輕量級的發布/訂閱訊息傳輸協議，廣泛用於物聯網應用。

### 基礎用法

#### 安裝 MQTT 客戶端庫

本專案已包含 `paho-mqtt`，如需單獨安裝：

```bash
uv pip install paho-mqtt
```

#### 基本 MQTT 連接和訂閱

```python
import streamlit as st
import paho.mqtt.client as mqtt
import json
import threading
import time

# MQTT 設定
MQTT_BROKER = "192.168.0.252"  # MQTT Broker IP 位址
MQTT_PORT = 1883
MQTT_USERNAME = "pi"  # 如果不需要認證，設為 None
MQTT_PASSWORD = "raspberry"  # 如果不需要認證，設為 None
MQTT_TOPIC = "sensor/temperature"  # 訂閱的主題

# 初始化 Session State
if 'mqtt_messages' not in st.session_state:
    st.session_state.mqtt_messages = []
if 'mqtt_client' not in st.session_state:
    st.session_state.mqtt_client = None
if 'mqtt_connected' not in st.session_state:
    st.session_state.mqtt_connected = False

# MQTT 回調函數
def on_connect(client, userdata, flags, rc):
    """連接成功時的回調"""
    if rc == 0:
        st.session_state.mqtt_connected = True
        st.session_state.mqtt_messages.append({
            'type': 'system',
            'message': '✅ MQTT 連接成功',
            'timestamp': time.time()
        })
        # 訂閱主題
        client.subscribe(MQTT_TOPIC)
    else:
        st.session_state.mqtt_messages.append({
            'type': 'error',
            'message': f'❌ MQTT 連接失敗，錯誤代碼: {rc}',
            'timestamp': time.time()
        })

def on_message(client, userdata, msg):
    """收到訊息時的回調"""
    try:
        payload = msg.payload.decode('utf-8')
        topic = msg.topic
        
        # 嘗試解析 JSON
        try:
            data = json.loads(payload)
        except:
            data = payload
        
        st.session_state.mqtt_messages.append({
            'type': 'message',
            'topic': topic,
            'data': data,
            'timestamp': time.time()
        })
    except Exception as e:
        st.session_state.mqtt_messages.append({
            'type': 'error',
            'message': f'處理訊息時發生錯誤: {str(e)}',
            'timestamp': time.time()
        })

def on_disconnect(client, userdata, rc):
    """斷開連接時的回調"""
    st.session_state.mqtt_connected = False
    st.session_state.mqtt_messages.append({
        'type': 'system',
        'message': '⚠️ MQTT 連接已斷開',
        'timestamp': time.time()
    })

# 連接 MQTT
def connect_mqtt():
    """建立 MQTT 連接"""
    if st.session_state.mqtt_client is None:
        client = mqtt.Client()
        
        # 設定認證（如果需要）
        if MQTT_USERNAME and MQTT_PASSWORD:
            client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        
        # 設定回調函數
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_disconnect = on_disconnect
        
        # 連接
        try:
            client.connect(MQTT_BROKER, MQTT_PORT, 60)
            client.loop_start()  # 在背景執行網路循環
            st.session_state.mqtt_client = client
        except Exception as e:
            st.error(f"連接失敗: {str(e)}")

# 斷開 MQTT 連接
def disconnect_mqtt():
    """斷開 MQTT 連接"""
    if st.session_state.mqtt_client:
        st.session_state.mqtt_client.loop_stop()
        st.session_state.mqtt_client.disconnect()
        st.session_state.mqtt_client = None
        st.session_state.mqtt_connected = False

# Streamlit 介面
st.title("MQTT 物聯網監控儀表板")

# 連接控制
col1, col2 = st.columns(2)
with col1:
    if st.button("連接 MQTT", disabled=st.session_state.mqtt_connected):
        connect_mqtt()
        st.rerun()

with col2:
    if st.button("斷開連接", disabled=not st.session_state.mqtt_connected):
        disconnect_mqtt()
        st.rerun()

# 顯示連接狀態
if st.session_state.mqtt_connected:
    st.success("🟢 MQTT 已連接")
else:
    st.error("🔴 MQTT 未連接")

# 顯示收到的訊息
st.subheader("收到的訊息")
if st.session_state.mqtt_messages:
    # 只顯示最近 50 條訊息
    recent_messages = st.session_state.mqtt_messages[-50:]
    for msg in reversed(recent_messages):
        if msg['type'] == 'message':
            st.json({
                '主題': msg['topic'],
                '資料': msg['data'],
                '時間': time.strftime('%H:%M:%S', time.localtime(msg['timestamp']))
            })
        else:
            st.write(f"[{time.strftime('%H:%M:%S', time.localtime(msg['timestamp']))}] {msg['message']}")
else:
    st.info("尚未收到任何訊息")

# 清除訊息按鈕
if st.button("清除訊息記錄"):
    st.session_state.mqtt_messages = []
    st.rerun()
```

#### 發布 MQTT 訊息

```python
import streamlit as st
import paho.mqtt.client as mqtt
import json

# 發布訊息到 MQTT
def publish_message(topic, message, qos=0, retain=False):
    """發布訊息到 MQTT Broker"""
    if st.session_state.mqtt_client and st.session_state.mqtt_connected:
        try:
            # 如果訊息是字典，轉換為 JSON
            if isinstance(message, dict):
                payload = json.dumps(message)
            else:
                payload = str(message)
            
            result = st.session_state.mqtt_client.publish(
                topic, 
                payload, 
                qos=qos, 
                retain=retain
            )
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                st.success(f"✅ 訊息已發布到 {topic}")
                return True
            else:
                st.error(f"❌ 發布失敗，錯誤代碼: {result.rc}")
                return False
        except Exception as e:
            st.error(f"發布訊息時發生錯誤: {str(e)}")
            return False
    else:
        st.warning("⚠️ 請先連接 MQTT")
        return False

# 在 Streamlit 中使用
st.subheader("發布訊息")

topic = st.text_input("主題", value="sensor/command")
message = st.text_area("訊息內容", value='{"action": "turn_on", "device": "led"}')

col1, col2 = st.columns(2)
with col1:
    qos = st.selectbox("QoS 等級", [0, 1, 2], index=0)
with col2:
    retain = st.checkbox("保留訊息", value=False)

if st.button("發布訊息"):
    publish_message(topic, message, qos=qos, retain=retain)
```

#### 即時數據視覺化

```python
import streamlit as st
import pandas as pd
import plotly.express as px
import time

# 在 on_message 回調中收集數據
if 'sensor_data' not in st.session_state:
    st.session_state.sensor_data = []

# 修改 on_message 函數以收集數據
def on_message(client, userdata, msg):
    """收到訊息時的回調（收集數據版本）"""
    try:
        payload = json.loads(msg.payload.decode('utf-8'))
        topic = msg.topic
        
        # 假設訊息格式為 {"temperature": 25.5, "humidity": 60}
        if 'temperature' in payload:
            st.session_state.sensor_data.append({
                'timestamp': time.time(),
                'temperature': payload.get('temperature'),
                'humidity': payload.get('humidity', 0)
            })
            
            # 只保留最近 100 筆數據
            if len(st.session_state.sensor_data) > 100:
                st.session_state.sensor_data.pop(0)
    except Exception as e:
        st.error(f"處理訊息錯誤: {str(e)}")

# 在 Streamlit 中顯示圖表
st.subheader("即時數據圖表")

if st.session_state.sensor_data:
    df = pd.DataFrame(st.session_state.sensor_data)
    df['time'] = pd.to_datetime(df['timestamp'], unit='s')
    
    # 溫度圖表
    fig_temp = px.line(df, x='time', y='temperature', 
                       title='溫度變化', labels={'temperature': '溫度 (°C)'})
    st.plotly_chart(fig_temp, use_container_width=True)
    
    # 濕度圖表
    if 'humidity' in df.columns:
        fig_humidity = px.line(df, x='time', y='humidity', 
                              title='濕度變化', labels={'humidity': '濕度 (%)'})
        st.plotly_chart(fig_humidity, use_container_width=True)
    
    # 顯示最新數據
    st.metric("當前溫度", f"{df['temperature'].iloc[-1]:.1f} °C")
    if 'humidity' in df.columns:
        st.metric("當前濕度", f"{df['humidity'].iloc[-1]:.1f} %")
else:
    st.info("等待數據...")
```

### 進階設定用法

#### 自動重連機制

```python
import streamlit as st
import paho.mqtt.client as mqtt
import time
import threading

class MQTTManager:
    """MQTT 管理器，包含自動重連功能"""
    
    def __init__(self, broker, port, username=None, password=None):
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password
        self.client = None
        self.connected = False
        self.reconnect_delay = 5  # 重連延遲（秒）
        self.max_reconnect_delay = 60
        self.reconnect_count = 0
        self.subscribed_topics = []
        
    def on_connect(self, client, userdata, flags, rc):
        """連接成功回調"""
        if rc == 0:
            self.connected = True
            self.reconnect_count = 0
            st.session_state.mqtt_messages.append({
                'type': 'system',
                'message': '✅ MQTT 連接成功',
                'timestamp': time.time()
            })
            
            # 重新訂閱所有主題
            for topic, qos in self.subscribed_topics:
                client.subscribe(topic, qos)
        else:
            self.connected = False
            error_messages = {
                1: "協議版本不正確",
                2: "客戶端 ID 無效",
                3: "伺服器不可用",
                4: "用戶名或密碼錯誤",
                5: "未授權"
            }
            error_msg = error_messages.get(rc, f"未知錯誤 ({rc})")
            st.session_state.mqtt_messages.append({
                'type': 'error',
                'message': f'❌ 連接失敗: {error_msg}',
                'timestamp': time.time()
            })
    
    def on_disconnect(self, client, userdata, rc):
        """斷開連接回調"""
        self.connected = False
        if rc != 0:
            # 非正常斷開，嘗試重連
            st.session_state.mqtt_messages.append({
                'type': 'system',
                'message': '⚠️ 連接意外斷開，嘗試重連...',
                'timestamp': time.time()
            })
            self.auto_reconnect()
    
    def on_message(self, client, userdata, msg):
        """訊息接收回調"""
        try:
            payload = json.loads(msg.payload.decode('utf-8'))
            topic = msg.topic
            
            st.session_state.mqtt_messages.append({
                'type': 'message',
                'topic': topic,
                'data': payload,
                'timestamp': time.time()
            })
        except Exception as e:
            st.error(f"處理訊息錯誤: {str(e)}")
    
    def connect(self):
        """建立連接"""
        try:
            self.client = mqtt.Client()
            
            if self.username and self.password:
                self.client.username_pw_set(self.username, self.password)
            
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.on_disconnect = self.on_disconnect
            
            # 設定遺囑訊息（Last Will and Testament）
            self.client.will_set("device/status", "offline", qos=1, retain=True)
            
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            
            return True
        except Exception as e:
            st.error(f"連接失敗: {str(e)}")
            return False
    
    def auto_reconnect(self):
        """自動重連"""
        def reconnect_loop():
            while not self.connected:
                delay = min(self.reconnect_delay * (2 ** self.reconnect_count), 
                           self.max_reconnect_delay)
                time.sleep(delay)
                
                try:
                    if self.client:
                        self.client.reconnect()
                    else:
                        self.connect()
                    self.reconnect_count += 1
                except:
                    pass
        
        thread = threading.Thread(target=reconnect_loop, daemon=True)
        thread.start()
    
    def subscribe(self, topic, qos=0):
        """訂閱主題"""
        if (topic, qos) not in self.subscribed_topics:
            self.subscribed_topics.append((topic, qos))
        
        if self.client and self.connected:
            self.client.subscribe(topic, qos)
    
    def publish(self, topic, payload, qos=0, retain=False):
        """發布訊息"""
        if self.client and self.connected:
            if isinstance(payload, dict):
                payload = json.dumps(payload)
            return self.client.publish(topic, payload, qos=qos, retain=retain)
        return None
    
    def disconnect(self):
        """斷開連接"""
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
            self.connected = False

# 使用範例
if 'mqtt_manager' not in st.session_state:
    st.session_state.mqtt_manager = MQTTManager(
        broker="192.168.0.252",
        port=1883,
        username="pi",
        password="raspberry"
    )

if st.button("連接 MQTT（自動重連）"):
    st.session_state.mqtt_manager.connect()
    st.session_state.mqtt_manager.subscribe("sensor/#", qos=1)
```

#### 多主題訂閱和過濾

```python
import streamlit as st
import re

class TopicFilter:
    """主題過濾器，支援萬用字元"""
    
    def __init__(self):
        self.filters = {}  # {pattern: callback}
    
    def add_filter(self, pattern, callback):
        """添加主題過濾器"""
        # 將 MQTT 萬用字元轉換為正則表達式
        regex_pattern = pattern.replace('+', '[^/]+').replace('#', '.*')
        self.filters[pattern] = {
            'regex': re.compile(f'^{regex_pattern}$'),
            'callback': callback
        }
    
    def match(self, topic):
        """匹配主題並執行對應的回調"""
        for pattern, filter_info in self.filters.items():
            if filter_info['regex'].match(topic):
                filter_info['callback'](topic)
                return True
        return False

# 使用範例
topic_filter = TopicFilter()

# 訂閱不同主題並設定不同的處理方式
def handle_temperature(topic):
    st.write(f"處理溫度數據: {topic}")

def handle_humidity(topic):
    st.write(f"處理濕度數據: {topic}")

topic_filter.add_filter("sensor/+/temperature", handle_temperature)
topic_filter.add_filter("sensor/+/humidity", handle_humidity)

# 在 on_message 中使用
def on_message(client, userdata, msg):
    topic = msg.topic
    topic_filter.match(topic)
```

#### QoS 等級和訊息確認

```python
import streamlit as st

# QoS 等級說明
st.subheader("MQTT QoS 等級")

st.markdown("""
**QoS 0 - 最多一次傳遞（Fire and Forget）**
- 訊息只發送一次，不保證送達
- 適用於：頻繁且可容忍丟失的數據（如感測器讀數）

**QoS 1 - 至少一次傳遞（At Least Once）**
- 保證訊息至少送達一次，可能重複
- 適用於：重要但可容忍重複的數據

**QoS 2 - 恰好一次傳遞（Exactly Once）**
- 保證訊息恰好送達一次
- 適用於：關鍵且不能重複的數據（如支付、控制指令）
""")

# 根據重要性選擇 QoS
def publish_with_appropriate_qos(topic, message, importance="normal"):
    """根據重要性選擇適當的 QoS"""
    qos_map = {
        "low": 0,      # 可容忍丟失
        "normal": 1,   # 重要但可重複
        "critical": 2  # 關鍵且不能重複
    }
    
    qos = qos_map.get(importance, 1)
    
    if st.session_state.mqtt_client:
        result = st.session_state.mqtt_client.publish(topic, message, qos=qos)
        
        # 等待發布確認（QoS > 0）
        if qos > 0:
            result.wait_for_publish()
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                st.success(f"✅ 訊息已確認送達 (QoS {qos})")
            else:
                st.error(f"❌ 訊息發布失敗")
        
        return result
```

#### 保留訊息和持久會話

```python
import streamlit as st

# 使用保留訊息儲存設備狀態
def publish_retained_message(topic, message):
    """發布保留訊息"""
    if st.session_state.mqtt_client:
        result = st.session_state.mqtt_client.publish(
            topic, 
            message, 
            qos=1, 
            retain=True  # 保留訊息
        )
        st.info("💾 訊息已保留，新訂閱者將立即收到此訊息")

# 使用持久會話（Clean Session = False）
def connect_with_persistent_session():
    """使用持久會話連接"""
    client_id = f"streamlit_client_{int(time.time())}"
    client = mqtt.Client(
        client_id=client_id,
        clean_session=False  # 持久會話
    )
    
    # 這樣即使斷線，未確認的訊息也會在重連後收到
    return client
```

#### 安全連接（TLS/SSL）

```python
import streamlit as st
import paho.mqtt.client as mqtt
import ssl

def connect_with_tls(broker, port, ca_cert=None, certfile=None, keyfile=None):
    """使用 TLS/SSL 安全連接"""
    client = mqtt.Client()
    
    # 設定 TLS
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    
    if ca_cert:
        context.load_verify_locations(ca_cert)
    
    if certfile and keyfile:
        context.load_cert_chain(certfile, keyfile)
    
    client.tls_set_context(context)
    
    # 連接（通常 TLS 使用 8883 端口）
    client.connect(broker, port, 60)
    client.loop_start()
    
    return client

# 使用範例
# client = connect_with_tls(
#     broker="mqtt.example.com",
#     port=8883,
#     ca_cert="/path/to/ca.crt"
# )
```

#### 完整範例：物聯網設備控制儀表板

```python
import streamlit as st
import paho.mqtt.client as mqtt
import json
import pandas as pd
import plotly.express as px
import time
from datetime import datetime

st.set_page_config(page_title="物聯網控制中心", layout="wide")

# MQTT 設定
MQTT_CONFIG = {
    'broker': st.sidebar.text_input("MQTT Broker", value="192.168.0.252"),
    'port': st.sidebar.number_input("端口", value=1883),
    'username': st.sidebar.text_input("用戶名", value="pi"),
    'password': st.sidebar.text_input("密碼", type="password", value="raspberry")
}

# 初始化
if 'mqtt_client' not in st.session_state:
    st.session_state.mqtt_client = None
if 'device_status' not in st.session_state:
    st.session_state.device_status = {}
if 'sensor_history' not in st.session_state:
    st.session_state.sensor_history = []

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        st.session_state.mqtt_client.subscribe("device/+/status", qos=1)
        st.session_state.mqtt_client.subscribe("sensor/+/data", qos=0)
        st.success("✅ 已連接")

def on_message(client, userdata, msg):
    topic_parts = msg.topic.split('/')
    try:
        data = json.loads(msg.payload.decode())
        
        if topic_parts[0] == 'device' and topic_parts[2] == 'status':
            device_id = topic_parts[1]
            st.session_state.device_status[device_id] = data
        
        elif topic_parts[0] == 'sensor' and topic_parts[2] == 'data':
            sensor_id = topic_parts[1]
            data['sensor_id'] = sensor_id
            data['timestamp'] = time.time()
            st.session_state.sensor_history.append(data)
            
            # 只保留最近 1000 筆
            if len(st.session_state.sensor_history) > 1000:
                st.session_state.sensor_history.pop(0)
    except:
        pass

# 連接控制
col1, col2 = st.columns(2)
with col1:
    if st.button("連接 MQTT"):
        if st.session_state.mqtt_client is None:
            client = mqtt.Client()
            client.username_pw_set(MQTT_CONFIG['username'], MQTT_CONFIG['password'])
            client.on_connect = on_connect
            client.on_message = on_message
            client.connect(MQTT_CONFIG['broker'], MQTT_CONFIG['port'], 60)
            client.loop_start()
            st.session_state.mqtt_client = client

with col2:
    if st.button("斷開連接"):
        if st.session_state.mqtt_client:
            st.session_state.mqtt_client.loop_stop()
            st.session_state.mqtt_client.disconnect()
            st.session_state.mqtt_client = None

# 設備控制面板
st.header("設備控制")

device_id = st.text_input("設備 ID", value="led_01")
command = st.selectbox("指令", ["on", "off", "toggle"])

if st.button("發送指令"):
    if st.session_state.mqtt_client:
        payload = {"command": command, "timestamp": time.time()}
        st.session_state.mqtt_client.publish(
            f"device/{device_id}/command",
            json.dumps(payload),
            qos=1
        )
        st.success(f"✅ 已發送指令: {command}")

# 設備狀態顯示
st.header("設備狀態")
if st.session_state.device_status:
    for device_id, status in st.session_state.device_status.items():
        col1, col2 = st.columns([1, 3])
        with col1:
            st.metric("設備", device_id)
        with col2:
            st.json(status)

# 感測器數據視覺化
st.header("感測器數據")
if st.session_state.sensor_history:
    df = pd.DataFrame(st.session_state.sensor_history)
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
    
    # 選擇感測器
    sensors = df['sensor_id'].unique()
    selected_sensor = st.selectbox("選擇感測器", sensors)
    
    sensor_df = df[df['sensor_id'] == selected_sensor]
    
    # 圖表
    if 'temperature' in sensor_df.columns:
        fig = px.line(sensor_df, x='datetime', y='temperature', 
                     title=f'{selected_sensor} 溫度變化')
        st.plotly_chart(fig, use_container_width=True)
    
    # 最新數據
    if not sensor_df.empty:
        latest = sensor_df.iloc[-1]
        cols = st.columns(len([c for c in latest.index if c not in ['sensor_id', 'timestamp', 'datetime']]))
        for i, col in enumerate([c for c in latest.index if c not in ['sensor_id', 'timestamp', 'datetime']]):
            with cols[i]:
                st.metric(col, latest[col])
```

### MQTT 最佳實踐

1. **選擇適當的 QoS 等級**
   - 感測器數據：QoS 0
   - 設備狀態：QoS 1
   - 關鍵控制指令：QoS 2

2. **使用主題層級結構**
   ```
   device/{device_id}/status
   device/{device_id}/command
   sensor/{sensor_id}/data
   ```

3. **實作自動重連機制**
   - 處理網路不穩定的情況
   - 使用指數退避策略

4. **使用保留訊息儲存狀態**
   - 新訂閱者可以立即獲得最新狀態
   - 適用於設備狀態、配置等

5. **安全考量**
   - 使用 TLS/SSL 加密連接
   - 實作用戶認證
   - 使用 ACL（存取控制列表）限制主題存取

6. **效能優化**
   - 避免在回調函數中執行耗時操作
   - 使用背景執行緒處理數據
   - 限制訊息歷史記錄的數量

## 參考資源

### 官方資源

- [Streamlit 官方文件](https://docs.streamlit.io/)
- [Streamlit API 參考](https://docs.streamlit.io/library/api-reference)
- [Streamlit 範例庫](https://streamlit.io/gallery)
- [Streamlit 社群論壇](https://discuss.streamlit.io/)
- [Streamlit GitHub](https://github.com/streamlit/streamlit)

### 圖表庫文件

- [Plotly Python](https://plotly.com/python/)
- [Altair 文件](https://altair-viz.github.io/)
- [Matplotlib 文件](https://matplotlib.org/)
- [Seaborn 文件](https://seaborn.pydata.org/)
- [Bokeh 文件](https://docs.bokeh.org/)

### 教學和範例

- [Streamlit 30 天挑戰](https://30days.streamlit.app/)
- [Awesome Streamlit](https://github.com/MarcSkovMadsen/awesome-streamlit)
- [Streamlit Components](https://streamlit.io/components)

### 安全性資源

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python 安全性最佳實踐](https://python.readthedocs.io/en/stable/library/security.html)
- [Streamlit 安全性指南](https://docs.streamlit.io/knowledge-base/deploy/deploy-securely)

## 本專案範例

查看 `lesson6/app.py` 以了解基本用法。

