"""
測試 YouTube 專注模式 Final版
驗證全螢幕模式下的覆蓋效果
"""

import tkinter as tk
from tkinter import messagebox
import threading
import time
import win32gui
import win32con
import ctypes

def test_fullscreen_overlay():
    """測試全螢幕覆蓋效果"""
    print("🧪 開始測試全螢幕覆蓋效果...")
    
    # 創建測試視窗
    test_root = tk.Tk()
    test_root.title("全螢幕測試視窗")
    test_root.configure(bg='red')
    
    # 設為全螢幕
    test_root.attributes('-fullscreen', True)
    test_root.attributes('-topmost', True)
    
    # 添加說明文字
    label = tk.Label(test_root, 
                    text="這是全螢幕測試視窗\n"
                         "如果專注模式有效，您應該看到邊緣覆蓋層\n"
                         "按 Escape 鍵退出全螢幕",
                    bg='red', fg='white', font=('Arial', 24))
    label.pack(expand=True)
    
    # 按Escape退出全螢幕
    def exit_fullscreen(event):
        test_root.attributes('-fullscreen', False)
        test_root.geometry("800x600")
    
    test_root.bind('<Escape>', exit_fullscreen)
    
    # 5秒後自動關閉
    def auto_close():
        time.sleep(5)
        try:
            test_root.destroy()
        except:
            pass
    
    threading.Thread(target=auto_close, daemon=True).start()
    
    print("📺 全螢幕測試視窗已開啟 (5秒後自動關閉)")
    test_root.mainloop()

def simulate_youtube_fullscreen():
    """模擬YouTube全螢幕環境"""
    print("🎬 模擬YouTube全螢幕環境...")
    
    # 創建模擬YouTube視窗
    youtube_window = tk.Tk()
    youtube_window.title("YouTube - Google Chrome")
    youtube_window.configure(bg='black')
    
    # 模擬YouTube播放界面
    video_frame = tk.Frame(youtube_window, bg='black', width=800, height=450)
    video_frame.pack(expand=True, fill=tk.BOTH, padx=50, pady=50)
    
    video_label = tk.Label(video_frame, 
                          text="🎥 模擬YouTube影片\n\n"
                               "點擊任意位置測試覆蓋阻擋\n"
                               "按 F 進入全螢幕模式\n"
                               "按 Escape 退出",
                          bg='black', fg='white', font=('Arial', 16))
    video_label.pack(expand=True)
    
    # 全螢幕切換
    def toggle_fullscreen(event):
        is_fullscreen = youtube_window.attributes('-fullscreen')
        youtube_window.attributes('-fullscreen', not is_fullscreen)
        if not is_fullscreen:
            print("📺 進入全螢幕模式 - 測試覆蓋層是否有效")
        else:
            print("🪟 退出全螢幕模式")
    
    def exit_fullscreen(event):
        youtube_window.attributes('-fullscreen', False)
        print("🪟 退出全螢幕模式")
    
    # 點擊檢測
    def on_click(event):
        print(f"🖱️ 檢測到點擊 - 位置: ({event.x}, {event.y})")
        if youtube_window.attributes('-fullscreen'):
            print("⚠️ 全螢幕模式下的點擊 - 檢查是否被覆蓋阻擋")
    
    youtube_window.bind('<f>', toggle_fullscreen)
    youtube_window.bind('<F>', toggle_fullscreen)
    youtube_window.bind('<Escape>', exit_fullscreen)
    youtube_window.bind('<Button-1>', on_click)
    video_label.bind('<Button-1>', on_click)
    
    youtube_window.focus_set()
    
    print("🎬 YouTube模擬視窗已開啟")
    print("   • 按 F 鍵進入/退出全螢幕")
    print("   • 按 Escape 退出全螢幕")
    print("   • 點擊檢測覆蓋效果")
    
    youtube_window.mainloop()

def test_window_priority():
    """測試視窗層級優先權"""
    print("🔝 測試視窗層級優先權...")
    
    def create_test_window(title, color, topmost_level):
        window = tk.Tk()
        window.title(title)
        window.configure(bg=color)
        window.geometry("300x200+100+100")
        
        if topmost_level == "highest":
            window.attributes('-topmost', True)
            # 使用Windows API設為最高層級
            window.update()
            try:
                hwnd = int(window.wm_frame(), 16)
                ctypes.windll.user32.SetWindowPos(
                    hwnd, -1, 0, 0, 0, 0,
                    win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW
                )
                print(f"✅ {title} 設為最高層級")
            except:
                print(f"❌ {title} 無法設為最高層級")
        elif topmost_level == "normal":
            window.attributes('-topmost', True)
            print(f"📌 {title} 設為普通置頂")
        
        label = tk.Label(window, text=title, bg=color, fg='white', font=('Arial', 14))
        label.pack(expand=True)
        
        return window
    
    # 創建不同層級的測試視窗
    windows = []
    
    # 普通置頂視窗
    normal_window = create_test_window("普通置頂視窗", "blue", "normal")
    windows.append(normal_window)
    
    time.sleep(1)
    
    # 最高層級視窗
    highest_window = create_test_window("最高層級視窗", "red", "highest")
    windows.append(highest_window)
    
    print("🎯 測試結果:")
    print("   • 藍色視窗: 普通置頂")
    print("   • 紅色視窗: 最高層級")
    print("   • 紅色視窗應該在藍色視窗上方")
    
    # 3秒後關閉所有視窗
    def close_all():
        time.sleep(3)
        for window in windows:
            try:
                window.destroy()
            except:
                pass
    
    threading.Thread(target=close_all, daemon=True).start()
    
    # 運行所有視窗
    for window in windows:
        window.update()
    
    time.sleep(4)

def main():
    print("=" * 60)
    print("🧪 YouTube 專注模式 Final版 - 測試工具")
    print("=" * 60)
    print()
    
    while True:
        print("請選擇測試項目:")
        print("1. 測試全螢幕覆蓋效果")
        print("2. 模擬YouTube全螢幕環境")
        print("3. 測試視窗層級優先權")
        print("4. 退出")
        print()
        
        choice = input("請輸入選項 (1-4): ").strip()
        
        if choice == "1":
            test_fullscreen_overlay()
        elif choice == "2":
            simulate_youtube_fullscreen()
        elif choice == "3":
            test_window_priority()
        elif choice == "4":
            print("👋 測試結束")
            break
        else:
            print("❌ 無效選項，請重新輸入")
        
        print("\n" + "-" * 40 + "\n")

if __name__ == "__main__":
    main()
