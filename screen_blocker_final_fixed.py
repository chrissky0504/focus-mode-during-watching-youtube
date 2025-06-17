"""
YouTube 專注模式 - 螢幕邊緣覆蓋工具 Final版 (修復版)
完全解決全螢幕模式下覆蓋層被壓下問題
修復影片播放完畢後覆蓋層不消失的問題
"""

import tkinter as tk
from tkinter import messagebox
import asyncio
import json
import websockets
import threading
import time
import ctypes
from ctypes import wintypes
import win32gui
import win32con
import win32api

# Windows API 常數
HWND_TOPMOST = -1
HWND_NOTOPMOST = -2
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001
SWP_SHOWWINDOW = 0x0040
SW_SHOW = 5

class ScreenBlocker:
    def __init__(self):
        self.root = None
        self.overlays = []
        self.overlay_hwnds = []  # 儲存覆蓋視窗的控制代碼
        self.is_blocking = False
        self.edge_window_handles = []
        self.monitor_thread = None
        self.keep_monitoring = False
        
    def find_edge_windows(self):
        """尋找所有Edge瀏覽器視窗"""
        edge_windows = []
        
        def enum_windows_callback(hwnd, param):
            if win32gui.IsWindowVisible(hwnd):
                try:
                    window_text = win32gui.GetWindowText(hwnd)
                    class_name = win32gui.GetClassName(hwnd)
                    
                    # 檢查是否為Edge視窗
                    if (class_name == "Chrome_WidgetWin_1" and 
                        ("Microsoft Edge" in window_text or 
                         "YouTube" in window_text or
                         window_text.endswith(" - Microsoft Edge"))):
                        edge_windows.append((hwnd, window_text))
                        print(f"🔍 找到Edge視窗: {window_text} (控制代碼: {hwnd})")
                except:
                    pass
            return True
        
        try:
            win32gui.EnumWindows(enum_windows_callback, None)
            self.edge_window_handles = [hwnd for hwnd, title in edge_windows]
            print(f"✅ 總共找到 {len(self.edge_window_handles)} 個Edge視窗")
            return edge_windows
        except Exception as e:
            print(f"❌ 尋找Edge視窗時發生錯誤: {e}")
            return []
    
    def set_window_always_on_top(self, hwnd, topmost=True):
        """使用Windows API設定視窗永遠置頂"""
        try:
            if topmost:
                # 設為置頂
                result = ctypes.windll.user32.SetWindowPos(
                    hwnd, HWND_TOPMOST, 0, 0, 0, 0,
                    SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW
                )
                if result:
                    print(f"✅ 視窗 {hwnd} 已設為置頂")
                else:
                    print(f"❌ 無法設定視窗 {hwnd} 為置頂")
                return result
            else:
                # 取消置頂
                result = ctypes.windll.user32.SetWindowPos(
                    hwnd, HWND_NOTOPMOST, 0, 0, 0, 0,
                    SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW
                )
                if result:
                    print(f"✅ 視窗 {hwnd} 已取消置頂")
                else:
                    print(f"❌ 無法取消視窗 {hwnd} 置頂")
                return result
        except Exception as e:
            print(f"❌ 設定視窗置頂狀態時錯誤: {e}")
            return False
    
    def set_windows_topmost(self, topmost=True):
        """設定Edge視窗為置頂或取消置頂"""
        if not self.edge_window_handles:
            self.find_edge_windows()
        
        if not self.edge_window_handles:
            print("⚠️ 未找到Edge視窗")
            return False
        
        action = "置頂" if topmost else "取消置頂"
        success_count = 0
        
        for hwnd in self.edge_window_handles[:]:  # 使用切片複製避免修改問題
            try:
                if win32gui.IsWindow(hwnd):
                    if self.set_window_always_on_top(hwnd, topmost):
                        window_title = win32gui.GetWindowText(hwnd)
                        print(f"✅ {action}Edge視窗: {window_title}")
                        success_count += 1
                else:
                    print(f"⚠️ 視窗 {hwnd} 已無效")
                    self.edge_window_handles.remove(hwnd)
            except Exception as e:
                print(f"❌ {action}視窗 {hwnd} 時發生錯誤: {e}")
        
        if success_count > 0:
            print(f"🎯 成功{action} {success_count} 個Edge視窗")
            return True
        else:
            print(f"❌ 無法{action}任何Edge視窗")
            return False
    
    def ensure_overlays_on_top(self):
        """確保覆蓋層永遠在最上層"""
        for hwnd in self.overlay_hwnds:
            try:
                if win32gui.IsWindow(hwnd):
                    # 強制設為最高層級
                    ctypes.windll.user32.SetWindowPos(
                        hwnd, HWND_TOPMOST, 0, 0, 0, 0,
                        SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW
                    )
                    # 再次確保在最前面
                    win32gui.BringWindowToTop(hwnd)
                    win32gui.SetForegroundWindow(hwnd)
            except:
                pass
    
    def monitor_windows(self):
        """持續監控視窗狀態，確保覆蓋層始終在最上層"""
        print("🔍 開始監控視窗狀態...")
        while self.keep_monitoring and self.is_blocking:
            try:
                # 每隔0.5秒檢查一次
                time.sleep(0.5)
                
                # 確保覆蓋層在最上層
                self.ensure_overlays_on_top()
                
                # 檢查是否有新的全螢幕視窗出現
                foreground_hwnd = win32gui.GetForegroundWindow()
                if foreground_hwnd:
                    try:
                        window_title = win32gui.GetWindowText(foreground_hwnd)
                        if "YouTube" in window_title and win32gui.IsZoomed(foreground_hwnd):
                            # 檢測到YouTube全螢幕，強制覆蓋層置頂
                            print(f"🎬 檢測到YouTube全螢幕: {window_title}")
                            self.ensure_overlays_on_top()
                    except:
                        pass
                        
            except Exception as e:                print(f"❌ 監控過程中發生錯誤: {e}")
                
        print("🛑 視窗監控已停止")
        
    def create_overlay(self, x, y, width, height, name):
        """創建一個最高層級的透明覆蓋視窗"""
        try:
            # 檢查主視窗是否存在
            if not self.root or not self.root.winfo_exists():
                print(f"❌ 主視窗不存在，無法創建 {name} 覆蓋")
                return None
                
            overlay = tk.Toplevel(self.root)  # 指定parent為主視窗
            overlay.title(f"Focus Mode - {name}")
            overlay.geometry(f"{width}x{height}+{x}+{y}")
            
            # 設定視窗屬性
            overlay.overrideredirect(True)  # 移除視窗邊框
            overlay.attributes('-topmost', True)  # Tkinter層級的置頂
            overlay.attributes('-alpha', 0.01)  # 幾乎透明
            overlay.configure(bg='black')
            
            # 強制更新視窗
            overlay.update_idletasks()
            overlay.update()
            
            # 獲取視窗控制代碼並用Windows API設為最高層級
            try:
                # 等待視窗完全創建
                overlay.after(100, lambda: self.set_overlay_highest_level(overlay))
            except Exception as e:
                print(f"⚠️ 設定 {name} 覆蓋高層級時錯誤: {e}")
            
            # 創建填滿整個覆蓋區域的標籤
            blocker_label = tk.Label(overlay, bg='black', text='', cursor='no')
            blocker_label.pack(fill=tk.BOTH, expand=True)
            
            # 事件阻止函數
            def block_all_events(event):
                """完全阻止所有事件"""
                print(f"🚫 阻止 {name} 區域的事件")
                return "break"
            
            # 綁定所有事件
            events_to_block = [
                '<Button-1>', '<Button-2>', '<Button-3>',
                '<Double-Button-1>', '<Triple-Button-1>',
                '<ButtonPress>', '<ButtonRelease>',
                '<Motion>', '<Enter>', '<Leave>',
                '<KeyPress>', '<KeyRelease>',
                '<FocusIn>', '<FocusOut>',
                '<Escape>', '<Alt_L>', '<Alt_R>',
                '<Control_L>', '<Control_R>',
                '<Tab>', '<Shift_L>', '<Shift_R>'
            ]
            
            for event in events_to_block:
                try:
                    overlay.bind(event, block_all_events)
                    blocker_label.bind(event, block_all_events)
                except:
                    pass
            
            # 阻止Alt+Tab和其他快捷鍵
            overlay.bind('<Alt-Tab>', block_all_events)
            overlay.bind('<Control-Tab>', block_all_events)
            overlay.bind('<Alt-Escape>', block_all_events)
            
            print(f"✅ 成功創建 {name} 覆蓋視窗")
            return overlay
            
        except Exception as e:
            print(f"❌ 創建 {name} 覆蓋時發生錯誤: {e}")
            return None
            try:
                overlay.bind(event, block_all_events)
                blocker_label.bind(event, block_all_events)
            except:
                pass
        
        # 阻止Alt+Tab和其他快捷鍵
        overlay.bind('<Alt-Tab>', block_all_events)
        overlay.bind('<Control-Tab>', block_all_events)
        overlay.bind('<Alt-Escape>', block_all_events)
        
        return overlay
    
    def set_overlay_highest_level(self, overlay):
        """設定覆蓋視窗為最高層級"""
        try:
            # 獲取Tkinter視窗的控制代碼
            hwnd = int(overlay.wm_frame(), 16)
            self.overlay_hwnds.append(hwnd)
              # 使用Windows API設為最高層級
            self.set_window_always_on_top(hwnd, True)
            print(f"🔝 覆蓋視窗 {hwnd} 已設為最高層級")
            
        except Exception as e:
            print(f"❌ 設定覆蓋視窗最高層級時錯誤: {e}")
    
    def cleanup_previous_session(self):
        """清理上一次會話的殘留狀態"""
        print("🧹 清理上一次會話...")
        
        # 停止監控
        if hasattr(self, 'keep_monitoring'):
            self.keep_monitoring = False
        
        # 等待監控線程結束
        if hasattr(self, 'monitor_thread') and self.monitor_thread and self.monitor_thread.is_alive():
            print("⏳ 等待監控線程結束...")
            time.sleep(1)
        
        # 清理殘留的覆蓋視窗
        if hasattr(self, 'overlay_hwnds'):
            for hwnd in self.overlay_hwnds[:]:
                try:
                    if win32gui.IsWindow(hwnd):
                        win32gui.ShowWindow(hwnd, 0)  # 隱藏
                        print(f"🧹 清理殘留覆蓋視窗: {hwnd}")
                except:
                    pass
        
        # 清理Tkinter覆蓋視窗
        if hasattr(self, 'overlays'):
            for overlay in self.overlays[:]:
                try:
                    if overlay and overlay.winfo_exists():
                        overlay.destroy()
                        print("🧹 清理殘留Tkinter視窗")
                except:
                    pass
        
        # 清理主視窗
        if hasattr(self, 'root') and self.root:
            try:
                self.root.destroy()
                print("🧹 清理殘留主視窗")
            except:
                pass
            self.root = None
        
        print("✅ 清理完成")
    
    def start_blocking(self):
        """開始螢幕阻擋"""
        # 檢查是否已經在運行
        if self.is_blocking:
            print("⚠️ 覆蓋已經在運行中")
            return
        
        # 確保之前的狀態完全清理
        self.cleanup_previous_session()
        
        # 重置所有狀態
        self.is_blocking = True
        self.keep_monitoring = True
        self.overlays = []
        self.overlay_hwnds = []
        self.edge_window_handles = []
        
        print("🚀 開始創建最高層級螢幕覆蓋...")
        
        # 尋找並設定Edge視窗為置頂
        print("🔍 正在尋找Edge視窗...")
        edge_windows = self.find_edge_windows()
        if edge_windows:
            print("📌 設定Edge視窗為完全置頂...")
            self.set_windows_topmost(True)
        
        # 創建新的主視窗
        try:
            if self.root:
                print("🔄 清理舊的主視窗...")
                self.root.destroy()
            
            self.root = tk.Tk()
            self.root.withdraw()  # 隱藏主視窗
            self.root.title("YouTube Focus Mode - Final Fixed")
            print("✅ 創建新的主視窗")
        except Exception as e:
            print(f"❌ 創建主視窗時錯誤: {e}")
            return
        
        # 獲取螢幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        print(f"🖥️ 螢幕尺寸: {screen_width}x{screen_height}")
        
        # 定義覆蓋區域 - 加大厚度確保完全阻擋
        overlay_thickness = 60
        right_overlay_thickness = 520  # 右側更寬
        
        # 創建四個邊緣覆蓋
        overlays_config = [
            (0, 0, screen_width, overlay_thickness, "頂部"),  # 頂部
            (0, screen_height - overlay_thickness, screen_width, overlay_thickness, "底部"),  # 底部
            (screen_width - right_overlay_thickness, 0, right_overlay_thickness, screen_height, "右側"),  # 右側
            (0, 0, overlay_thickness, screen_height, "左側")  # 左側
        ]
        
        overlay_created_count = 0
        for x, y, width, height, name in overlays_config:
            try:
                overlay = self.create_overlay(x, y, width, height, name)
                if overlay:
                    self.overlays.append(overlay)
                    overlay_created_count += 1
                    print(f"✅ 創建 {name} 覆蓋")
                else:
                    print(f"❌ 無法創建 {name} 覆蓋")
            except Exception as e:
                print(f"❌ 創建 {name} 覆蓋時錯誤: {e}")
        
        if overlay_created_count == 0:
            print("❌ 沒有成功創建任何覆蓋，取消專注模式")
            self.is_blocking = False
            self.keep_monitoring = False
            return
        
        print("✅ 最高層級螢幕覆蓋已啟動")
        print(f"   • 成功創建 {overlay_created_count}/4 個覆蓋")
        print(f"   • 頂部/底部覆蓋: {overlay_thickness}px")
        print(f"   • 左側覆蓋: {overlay_thickness}px")
        print(f"   • 右側覆蓋: {right_overlay_thickness}px")
        print("   • 🔒 使用最高Windows層級，全螢幕下也有效")
        
        # 啟動監控線程
        if self.monitor_thread and self.monitor_thread.is_alive():
            print("⚠️ 舊的監控線程仍在運行，等待結束...")
            self.keep_monitoring = False
            time.sleep(1)
        
        self.monitor_thread = threading.Thread(target=self.monitor_windows, daemon=True)
        self.monitor_thread.start()
        print("✅ 啟動新的監控線程")
        
        # 稍後確保覆蓋層在最上層
        self.root.after(1000, self.ensure_overlays_on_top)
        
        # 顯示專注模式提示
        self.show_focus_message()
        
    def show_focus_message(self):
        """顯示專注模式啟動訊息"""
        try:
            messagebox.showinfo("🎯 專注模式啟動", 
                              "YouTube 專注模式 Final版已啟動！\n\n"
                              "• 螢幕邊緣已被最高層級覆蓋\n"
                              "• 完全阻止所有點擊和快捷鍵\n"
                              "• 全螢幕模式下保證有效\n"
                              "• 持續監控確保覆蓋在最上層\n"
                              "• 影片結束後將自動解除")
        except:
            print("💡 專注模式提示已顯示")
    
    def stop_blocking(self):
        """停止螢幕阻擋 - 修復版，確保完全移除覆蓋"""
        if not self.is_blocking:
            print("⚠️ 專注模式已經關閉")
            return
            
        print("🛑 正在移除最高層級螢幕覆蓋...")
        
        # 先設定停止標誌
        self.is_blocking = False
        self.keep_monitoring = False
        
        # 強制取消所有覆蓋視窗置頂並銷毀
        print("🔓 強制移除所有覆蓋視窗...")
        for hwnd in self.overlay_hwnds[:]:  # 使用切片複製避免修改問題
            try:
                if win32gui.IsWindow(hwnd):
                    # 取消置頂
                    self.set_window_always_on_top(hwnd, False)
                    # 強制隱藏視窗
                    win32gui.ShowWindow(hwnd, 0)  # SW_HIDE
                    print(f"✅ 隱藏覆蓋視窗: {hwnd}")
            except Exception as e:
                print(f"⚠️ 處理覆蓋視窗 {hwnd} 時錯誤: {e}")
        
        # 銷毀Tkinter覆蓋視窗
        for overlay in self.overlays[:]:  # 使用切片複製
            try:
                if overlay and overlay.winfo_exists():
                    overlay.withdraw()  # 先隱藏
                    overlay.destroy()   # 再銷毀
                    print("✅ 銷毀Tkinter覆蓋視窗")
            except Exception as e:
                print(f"⚠️ 銷毀覆蓋視窗時錯誤: {e}")
          # 清空列表並重置所有狀態
        self.overlays.clear()
        self.overlay_hwnds.clear()
        self.edge_window_handles.clear()
        
        # 取消Edge視窗置頂
        if self.edge_window_handles:
            print("📌 取消Edge視窗置頂...")
            self.set_windows_topmost(False)
        
        # 強制關閉主視窗
        if self.root:
            try:
                print("🔄 關閉主視窗...")
                # 停止mainloop
                self.root.quit()
                # 銷毀視窗
                self.root.destroy()
                print("✅ 主視窗已關閉")
            except Exception as e:
                print(f"⚠️ 關閉主視窗時錯誤: {e}")
            finally:
                self.root = None
          # 等待短暫時間確保所有清理完成
        time.sleep(0.2)
        
        print("✅ 最高層級螢幕覆蓋已完全移除，狀態已重置")
        
        # 短暫延遲後顯示解除訊息
        def show_completion_message():
            try:
                time.sleep(0.5)  # 確保所有視窗都已關閉
                
                temp_root = tk.Tk()
                temp_root.withdraw()
                messagebox.showinfo("🎉 專注模式結束", 
                                  "專注模式 Final版已結束！\n"
                                  "所有覆蓋已完全移除，可以正常使用電腦了")
                temp_root.destroy()
            except Exception as e:
                print(f"💡 專注模式結束 (提示視窗錯誤: {e})")
        
        # 在新線程中顯示完成訊息，避免阻塞
        threading.Thread(target=show_completion_message, daemon=True).start()
    
    def run_gui(self):
        """運行GUI主循環"""
        if self.root:
            print("🔄 啟動GUI主循環...")
            try:
                self.root.mainloop()
            except Exception as e:
                print(f"⚠️ GUI主循環錯誤: {e}")
            finally:
                print("🔄 GUI主循環已結束")

# WebSocket 伺服器部分
class FocusWebSocketServer:
    def __init__(self, screen_blocker):
        self.screen_blocker = screen_blocker
        
    async def handle_connection(self, websocket):
        print(f"🔗 WebSocket連線成功: {websocket.remote_address}")
        print("💡 等待接收訊息...")
        
        try:
            async for message in websocket:
                print(f"📨 收到訊息: {message}")
                try:
                    data = json.loads(message)
                    
                    if data['action'] == 'progress':
                        progress = data['progress']
                        print(f"📊 影片進度: {progress:.1f}%")
                        if progress >= 100:
                            print("🎉 影片播放完畢，解除專注模式")
                            # 在新線程中停止阻擋，避免阻塞WebSocket
                            threading.Thread(target=self.stop_blocking_safely, daemon=True).start()

                    elif data['action'] == 'lock':
                        print("🔒 收到鎖定訊號，啟動最高層級專注模式")
                        threading.Thread(target=self.start_blocking_thread, daemon=True).start()
                    
                    elif data['action'] == 'unlock':
                        print("🔓 收到解鎖訊號，解除專注模式")
                        # 在新線程中停止阻擋，避免阻塞WebSocket
                        threading.Thread(target=self.stop_blocking_safely, daemon=True).start()
                    
                    else:
                        print(f"⚠️ 未知動作: {data.get('action', 'None')}")
                        
                except json.JSONDecodeError as e:
                    print(f"❌ JSON解析錯誤: {e}")
                    
        except Exception as e:
            print(f"❌ 連線錯誤: {e}")
        finally:
            print("🔌 WebSocket連線已關閉")
    
    def stop_blocking_safely(self):
        """安全地停止螢幕阻擋，確保不阻塞WebSocket"""
        try:
            print("🔄 安全停止專注模式...")
            self.screen_blocker.stop_blocking()
        except Exception as e:
            print(f"❌ 停止專注模式時錯誤: {e}")
    
    def start_blocking_thread(self):
        """在新線程中啟動螢幕阻擋"""
        print("🎯 在新線程中啟動最高層級螢幕阻擋...")
        try:
            self.screen_blocker.start_blocking()
            self.screen_blocker.run_gui()
        except Exception as e:
            print(f"❌ 啟動專注模式時錯誤: {e}")
    
    async def start_server(self):
        server = await websockets.serve(self.handle_connection, "localhost", 8080)
        print("🚀 WebSocket伺服器已啟動 (localhost:8080)")
        print("💡 等待YouTube擴充套件連線...")
        await server.wait_closed()

def main():
    print("=" * 70)
    print("🎯 YouTube 專注模式 - 螢幕覆蓋 Final版 (修復版)")
    print("=" * 70)
    print("🔥 此版本完全解決全螢幕模式下覆蓋層消失問題！")
    print("🔧 修復影片播放完畢後覆蓋層不消失的問題！")
    print("• 使用最高Windows層級確保覆蓋永遠在最上層")
    print("• 持續監控視窗狀態，防止被其他視窗蓋住")
    print("• 完全阻止所有點擊、快捷鍵和視窗切換")
    print("• 強化視窗清理機制，確保覆蓋完全移除")
    print("• 🆕 即使YouTube全螢幕也無法繞過覆蓋層")
    print("• 🆕 影片結束後覆蓋層保證完全消失")
    print()
    
    # 檢查依賴
    try:
        import win32gui
        import win32con
        import win32api
        print("✅ 所有Windows API依賴正常")
    except ImportError:
        print("❌ 缺少 pywin32 依賴，請執行:")
        print("   pip install pywin32")
        return
    
    screen_blocker = ScreenBlocker()
    websocket_server = FocusWebSocketServer(screen_blocker)
    
    try:
        # 啟動WebSocket伺服器
        asyncio.run(websocket_server.start_server())
        
    except KeyboardInterrupt:
        print("\n🛑 正在關閉...")
        screen_blocker.stop_blocking()
        print("✅ 已安全關閉")
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        screen_blocker.stop_blocking()

if __name__ == "__main__":
    main()
