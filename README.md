# YouTube 專注模式 Edge 擴充套件

這是一個協助用戶專注觀看 YouTube 影片的系統，結合 Edge 瀏覽器擴充套件與本地 Python 程式。

## 🆕 v3 新功能

- ✅ **Edge 視窗自動置頂**：專注模式時自動將 Edge 視窗設為完全置頂
- ✅ **智慧視窗管理**：自動尋找所有 Edge 瀏覽器視窗
- ✅ **自動取消置頂**：專注模式結束時自動恢復正常視窗層級
- ✅ **加寬右側覆蓋**：右側覆蓋層擴增至 550px，更有效防止誤觸
- ✅ **全螢幕相容**：修正全螢幕模式下的點擊穿透問題

## 系統組成

### Edge 擴充套件
- `manifest.json` - 擴充套件設定
- `content.js` - YouTube 頁面腳本
- `background.js` - 背景服務
- `popup.html/js` - 彈出視窗介面
- `options.html/js` - 設定頁面

### Python 後端
- `screen_blocker_v3.py` - **主程式** (最新版，包含視窗置頂功能)
- `focus_server_v2.py` - WebSocket 伺服器 (簡化版)
- `install_dependencies.py` - 依賴安裝器
- `test_edge_topmost.py` - Edge 視窗管理測試工具

## 快速安裝

### 1. 安裝 Python 依賴
```bash
pip install websockets pywin32
```

### 2. 安裝 Edge 擴充套件
1. 開啟 Edge 瀏覽器
2. 前往 `edge://extensions/`
3. 開啟「開發人員模式」
4. 點擊「載入解壓縮」
5. 選擇此專案的 `focus` 資料夾

## 使用方式

### 1. 啟動後端程式
```bash
# 啟動主程式 (推薦)
python screen_blocker_final_fixed.py

# 或啟動簡化版伺服器
python focus_server_v2.py
```

### 2. 使用專注模式
1. 開啟 YouTube 影片
2. 點擊 Edge 工具列上的專注模式圖示
3. 點擊「開始專注模式」按鈕
4. 系統將自動：
   - 🔒 建立螢幕邊緣覆蓋層
   - 📌 將 Edge 視窗設為完全置頂
   - 🚫 阻止所有點擊切換視窗的行為

### 3. 結束專注模式
專注模式會在以下情況自動結束：
- ✅ YouTube 影片播放完畢
- ✅ 手動點擊「解除專注模式」按鈕

系統會自動：
- 📌 取消 Edge 視窗置頂
- 🔓 移除螢幕覆蓋層
- 💬 顯示結束提示

## 測試工具

### Edge 視窗管理測試
```bash
python test_edge_topmost.py
```
此工具會：
1. 尋找所有 Edge 視窗
2. 測試置頂功能
3. 5秒後自動取消置頂

### 緊急修復工具
如果視窗卡在置頂狀態：
```bash
python fix_edge_window.py      # 修復所有 Edge 視窗
python remove_topmost.py       # 移除所有置頂視窗
python quick_fix_topmost.py    # 快速修復工具
```

## 覆蓋區域配置

screen_blocker_v3.py 的覆蓋設定：
- **頂部**：50px 高度，阻止點擊其他視窗標題列
- **底部**：50px 高度，阻止點擊工作列
- **左側**：50px 寬度，阻止左側操作
- **右側**：550px 寬度，有效阻止視窗切換手勢

## 故障排除

### 常見問題

1. **找不到 Edge 視窗**
   - 確保 Edge 瀏覽器已開啟
   - 確保有開啟 YouTube 或任何網頁
   - 檢查是否使用正確的 Edge 版本（非 IE 模式）

2. **視窗無法置頂**
   - 以系統管理員身分執行 Python 程式
   - 檢查是否有其他軟體衝突

3. **依賴安裝失敗**
   - 確保 Python 版本 3.7+
   - 嘗試升級 pip：`python -m pip install --upgrade pip`
   - 手動安裝：`pip install websockets pywin32`

### 系統需求
- Windows 10/11
- Python 3.7+
- Microsoft Edge 瀏覽器
- 網路連線（安裝依賴時）

## 開發資訊

### 檔案結構
```
focus/
├── manifest.json          # 擴充套件設定
├── content.js             # YouTube 頁面腳本
├── background.js          # 背景服務
├── popup.html/js          # 彈出視窗
├── options.html/js        # 設定頁面
├── styles.css             # 樣式表
├── screen_blocker_v3.py   # 主程式 ⭐
├── focus_server_v2.py     # 簡化伺服器
├── install_dependencies.py # 依賴安裝器
├── test_edge_topmost.py   # 測試工具
└── 各種修復工具...
```

### 通訊協定
擴充套件與 Python 程式透過 WebSocket (localhost:8080) 通訊：

```json
{
  "action": "lock",        // 啟動專注模式
  "action": "unlock",      // 解除專注模式  
  "action": "progress",    // 影片進度更新
  "progress": 75.5         // 進度百分比
}
```

## 更新日誌

### v3.0 (最新)
- 🆕 加入 Edge 視窗自動置頂/取消置頂功能
- 🆕 智慧尋找所有 Edge 瀏覽器視窗
- 🆕 右側覆蓋層加寬至 550px
- 🔧 修正全螢幕模式點擊穿透問題
- 🔧 改善錯誤處理和用戶提示

### v2.0
- 加入螢幕邊緣覆蓋功能
- 修正各種視窗管理問題
- 改善 WebSocket 通訊穩定性

### v1.0
- 基本專注模式功能
- Edge 擴充套件開發
- YouTube 影片進度偵測

---

🎯 **專注模式讓您全心投入 YouTube 學習！**