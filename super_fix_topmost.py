"""
超強力修復工具 - 完全解除所有視窗置頂狀態
解決專注模式可能留下的任何置頂問題
"""

import win32gui
import win32con
import ctypes
import time

# Windows API 常數
HWND_NOTOPMOST = -2
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001
SWP_SHOWWINDOW = 0x0040

def find_all_topmost_windows():
    """找到所有置頂視窗"""
    topmost_windows = []
    
    def enum_windows_callback(hwnd, param):
        if win32gui.IsWindowVisible(hwnd):
            try:
                # 檢查視窗是否為置頂
                ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
                if ex_style & win32con.WS_EX_TOPMOST:
                    window_text = win32gui.GetWindowText(hwnd)
                    class_name = win32gui.GetClassName(hwnd)
                    topmost_windows.append((hwnd, window_text, class_name))
            except:
                pass
        return True
    
    win32gui.EnumWindows(enum_windows_callback, None)
    return topmost_windows

def remove_topmost_from_window(hwnd, window_title):
    """移除單個視窗的置頂狀態"""
    try:
        # 方法1: 使用SetWindowPos
        result1 = win32gui.SetWindowPos(
            hwnd, HWND_NOTOPMOST, 0, 0, 0, 0,
            SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW
        )
        
        # 方法2: 使用ctypes直接調用
        result2 = ctypes.windll.user32.SetWindowPos(
            hwnd, HWND_NOTOPMOST, 0, 0, 0, 0,
            SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW
        )
        
        # 方法3: 修改視窗樣式
        try:
            ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            new_ex_style = ex_style & ~win32con.WS_EX_TOPMOST
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_ex_style)
        except:
            pass
        
        if result1 or result2:
            print(f"✅ 成功移除置頂: {window_title} (控制代碼: {hwnd})")
            return True
        else:
            print(f"❌ 無法移除置頂: {window_title} (控制代碼: {hwnd})")
            return False
            
    except Exception as e:
        print(f"❌ 移除置頂時發生錯誤: {e}")
        return False

def force_remove_all_topmost():
    """強制移除所有置頂視窗"""
    print("🔍 正在搜尋所有置頂視窗...")
    
    # 多次搜尋確保找到所有視窗
    all_topmost = set()
    for i in range(3):
        topmost_windows = find_all_topmost_windows()
        for hwnd, title, class_name in topmost_windows:
            all_topmost.add((hwnd, title, class_name))
        time.sleep(0.1)
    
    if not all_topmost:
        print("✅ 沒有發現置頂視窗")
        return
    
    print(f"🎯 發現 {len(all_topmost)} 個置頂視窗:")
    
    success_count = 0
    for hwnd, window_title, class_name in all_topmost:
        print(f"   📝 {window_title} ({class_name}) - 控制代碼: {hwnd}")
        
        # 檢查視窗是否仍然存在且置頂
        try:
            if win32gui.IsWindow(hwnd):
                ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
                if ex_style & win32con.WS_EX_TOPMOST:
                    if remove_topmost_from_window(hwnd, window_title):
                        success_count += 1
                else:
                    print(f"ℹ️ 視窗已經不是置頂: {window_title}")
            else:
                print(f"⚠️ 視窗已經不存在: {window_title}")
        except Exception as e:
            print(f"❌ 檢查視窗時錯誤: {e}")
    
    print(f"\n🎉 完成！成功移除 {success_count} 個視窗的置頂狀態")
    
    # 驗證結果
    print("\n🔍 驗證移除結果...")
    time.sleep(0.5)
    remaining_topmost = find_all_topmost_windows()
    
    # 過濾掉系統視窗
    user_topmost = []
    for hwnd, title, class_name in remaining_topmost:
        # 跳過一些系統視窗
        if (title and 
            "Focus Mode" not in title and
            "YouTube 專注模式" not in title and
            class_name not in ["Shell_TrayWnd", "Progman", "WorkerW"]):
            user_topmost.append((hwnd, title, class_name))
    
    if user_topmost:
        print(f"⚠️ 仍有 {len(user_topmost)} 個用戶視窗保持置頂:")
        for hwnd, title, class_name in user_topmost:
            print(f"   📌 {title} ({class_name})")
        print("這可能是正常的系統行為或其他程式設定的置頂")
    else:
        print("✅ 所有用戶視窗的置頂狀態都已成功移除！")

def main():
    print("=" * 60)
    print("🔧 超強力視窗置頂修復工具")
    print("=" * 60)
    print("此工具將:")
    print("• 掃描所有置頂視窗")
    print("• 強制移除置頂狀態")
    print("• 使用多種方法確保完全移除")
    print("• 驗證移除結果")
    print()
    
    try:
        force_remove_all_topmost()
        
        print("\n" + "=" * 60)
        print("🎯 修復完成！")
        print("如果您的Edge瀏覽器或其他視窗仍有問題，")
        print("可以嘗試重新啟動該程式。")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ 修復過程中發生錯誤: {e}")
    
    input("\n按 Enter 鍵退出...")

if __name__ == "__main__":
    main()
