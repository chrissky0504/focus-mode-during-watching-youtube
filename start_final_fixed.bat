@echo off
echo ========================================
echo   YouTube 專注模式 Final修復版 啟動器
echo ========================================
echo.
echo 🔥 此版本完全解決所有已知問題！
echo ✅ 全螢幕模式下覆蓋層保證有效
echo ✅ 影片播放完畢後覆蓋層完全消失
echo ✅ 第二次啟動專注模式正常工作
echo.
echo 正在啟動伺服器...
echo.

cd /d "%~dp0"

REM 檢查Python是否安裝
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，請先安裝Python
    pause
    exit /b 1
)

REM 檢查依賴
echo 🔍 檢查依賴套件...
python -c "import websockets, win32gui, win32con, win32api, ctypes" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ 缺少依賴套件，正在安裝...
    pip install websockets pywin32
    echo.
)

REM 啟動Final修復版伺服器
echo 🚀 啟動 YouTube 專注模式 Final修復版...
echo.
echo 💡 使用說明:
echo    1. 確保Edge擴充套件已安裝並啟用
echo    2. 開啟YouTube影片
echo    3. 點擊擴充套件圖示啟動專注模式
echo    4. 即使全螢幕也能完全阻擋分心
echo    5. 影片結束後覆蓋層會完全消失
echo    6. 可以多次啟動和關閉專注模式
echo.
echo 🧪 測試工具: 另外執行 test_second_start.py 可測試多次啟動
echo.
echo 按 Ctrl+C 可隨時停止伺服器
echo.

python screen_blocker_final_fixed.py

echo.
echo 🛑 伺服器已停止
pause
