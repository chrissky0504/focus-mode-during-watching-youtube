# YouTube 專注模式 Final版 - 完整使用指南

## 🔥 Final版重大改進

### 完全解決全螢幕問題
- **使用最高Windows層級**: 覆蓋層永遠在所有視窗之上，包括全螢幕YouTube
- **持續監控機制**: 實時檢測視窗狀態，確保覆蓋層始終有效
- **強化事件阻擋**: 完全攔截所有滑鼠和鍵盤事件
- **多重保險機制**: 使用多種API確保覆蓋層不會被壓下

### 新增功能
- ✅ **全螢幕模式完全支援**: YouTube全螢幕時覆蓋層依然有效
- ✅ **Edge視窗自動置頂**: 專注模式時Edge永遠在最上層
- ✅ **智能視窗監控**: 自動檢測並應對視窗狀態變化
- ✅ **加強版覆蓋**: 更厚的邊緣覆蓋，更強的阻擋效果
- ✅ **完整的清理機制**: 結束時自動移除所有置頂狀態

## 📁 檔案說明

### 核心檔案 (必要)
- `screen_blocker_final.py` - **Final版主程式**，解決所有已知問題
- `manifest.json` - Edge擴充套件設定檔
- `background.js` - 擴充套件背景腳本
- `content.js` - YouTube頁面注入腳本
- `popup.html/js` - 擴充套件彈出視窗
- `start_final.bat` - **Final版專用啟動器**

### 修復工具
- `super_fix_topmost.py` - **超強力修復工具**，解除所有置頂狀態
- `test_final_version.py` - Final版測試工具

### 舊版檔案 (可選保留)
- `screen_blocker_v3.py` - 舊版主程式
- `focus_server_v2.py` - 舊版伺服器
- 其他修復工具和測試檔案

## 🚀 完整安裝步驟

### 1. 準備環境
```bash
# 安裝Python依賴
pip install websockets pywin32

# 或使用requirements.txt (如果存在)
pip install -r requirements.txt
```

### 2. 安裝Edge擴充套件
1. 開啟Edge瀏覽器
2. 進入 `edge://extensions/`
3. 開啟「開發人員模式」
4. 點擊「載入解壓縮的擴充功能」
5. 選擇 `focus` 資料夾
6. 確認擴充套件已啟用

### 3. 啟動Final版系統
**方法一: 使用專用啟動器 (推薦)**
```bash
# 雙擊執行
start_final.bat
```

**方法二: 直接執行**
```bash
python screen_blocker_final.py
```

## 🎯 使用方式

### 基本操作
1. **啟動伺服器**: 執行 `start_final.bat`
2. **開啟YouTube**: 在Edge中開啟YouTube影片
3. **啟動專注模式**: 點擊擴充套件圖示 → 點擊「啟動專注模式」
4. **享受專注**: 系統會自動阻擋所有分心操作
5. **自動結束**: 影片播放完畢自動解除，或手動點擊「解除專注模式」

### 全螢幕模式使用
1. 先啟動專注模式
2. 進入YouTube全螢幕 (按F鍵或點擊全螢幕按鈕)
3. **覆蓋層依然有效**: 螢幕邊緣會被完全阻擋
4. **無法切換視窗**: 所有Alt+Tab、點擊等操作都被阻止
5. 退出全螢幕後覆蓋層繼續有效

## 🔧 進階功能

### 手動視窗控制
```python
# 如果需要手動控制Edge視窗置頂
from screen_blocker_final import ScreenBlocker
blocker = ScreenBlocker()
blocker.find_edge_windows()
blocker.set_windows_topmost(True)  # 置頂
blocker.set_windows_topmost(False) # 取消置頂
```

### 緊急修復
如果系統出現問題 (視窗卡住置頂等):
```bash
# 執行超強力修復工具
python super_fix_topmost.py
```

### 測試功能
```bash
# 測試Final版功能
python test_final_version.py
```

## ⚡ 效果對比

| 功能 | v3版本 | Final版 |
|------|--------|---------|
| 一般模式阻擋 | ✅ | ✅ |
| 全螢幕模式阻擋 | ❌ 覆蓋層消失 | ✅ 完全有效 |
| Edge視窗置頂 | ⚠️ 部分支援 | ✅ 完全支援 |
| 視窗監控 | ❌ | ✅ 實時監控 |
| 清理機制 | ⚠️ 可能殘留 | ✅ 完整清理 |
| 多螢幕支援 | ✅ | ✅ |
| 穩定性 | ⚠️ 中等 | ✅ 非常穩定 |

## 🐛 疑難排解

### 問題1: 全螢幕時覆蓋層消失
**Final版已解決此問題**，如果仍有問題:
1. 確認使用的是 `screen_blocker_final.py`
2. 檢查Windows API依賴: `pip install pywin32`
3. 以管理員權限執行

### 問題2: Edge視窗無法置頂
```bash
# 執行修復工具
python super_fix_topmost.py
```

### 問題3: 擴充套件連線失敗
1. 確認伺服器正在運行 (localhost:8080)
2. 檢查Edge擴充套件是否正確安裝
3. 重新載入YouTube頁面

### 問題4: 系統卡住或視窗異常
```bash
# 立即執行緊急修復
python super_fix_topmost.py
```

## 📊 技術架構

### Final版核心技術
1. **多層級視窗管理**: 使用Windows API確保最高層級
2. **實時監控系統**: 持續檢測視窗狀態變化
3. **事件完全攔截**: 阻擋所有可能的分心操作
4. **智能清理機制**: 自動恢復所有系統狀態

### 系統要求
- Windows 10/11
- Python 3.7+
- Microsoft Edge瀏覽器
- pywin32套件
- websockets套件

## 🎉 Final版優勢

1. **100% 全螢幕支援**: 完全解決覆蓋層消失問題
2. **零殘留**: 結束時完全恢復系統狀態
3. **超強穩定性**: 經過全面測試和優化
4. **智能監控**: 自動應對各種情況
5. **用戶友好**: 簡單易用，無需複雜設定

Final版是目前最完整、最穩定的版本，強烈建議使用！
