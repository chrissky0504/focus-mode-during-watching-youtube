"""
測試第二次專注模式啟動
驗證覆蓋層能否正常重新創建
"""

import asyncio
import json
import websockets
import time
import threading

class FocusModeTester:
    def __init__(self):
        self.websocket = None
        
    async def connect_to_server(self):
        """連接到專注模式伺服器"""
        try:
            self.websocket = await websockets.connect("ws://localhost:8080")
            print("✅ 成功連接到專注模式伺服器")
            return True
        except Exception as e:
            print(f"❌ 無法連接到伺服器: {e}")
            print("請確保專注模式伺服器正在運行")
            return False
    
    async def send_command(self, action, **kwargs):
        """發送命令到伺服器"""
        if not self.websocket:
            print("❌ 未連接到伺服器")
            return False
            
        try:
            message = {"action": action, **kwargs}
            await self.websocket.send(json.dumps(message))
            print(f"📤 發送命令: {action}")
            return True
        except Exception as e:
            print(f"❌ 發送命令失敗: {e}")
            return False
    
    async def test_multiple_sessions(self):
        """測試多次啟動專注模式"""
        if not await self.connect_to_server():
            return
        
        try:
            print("\n" + "="*50)
            print("🧪 開始測試多次專注模式啟動")
            print("="*50)
            
            for session in range(1, 4):  # 測試3次
                print(f"\n🔄 第 {session} 次專注模式測試")
                print("-" * 30)
                
                # 啟動專注模式
                print("1️⃣ 啟動專注模式...")
                await self.send_command("lock")
                await asyncio.sleep(3)  # 等待3秒讓覆蓋層創建
                
                # 模擬影片進度
                print("2️⃣ 模擬影片播放...")
                for progress in [25, 50, 75]:
                    await self.send_command("progress", progress=progress)
                    await asyncio.sleep(1)
                
                # 模擬影片結束
                print("3️⃣ 模擬影片結束...")
                await self.send_command("progress", progress=100)
                await asyncio.sleep(3)  # 等待覆蓋層移除
                
                print(f"✅ 第 {session} 次測試完成")
                
                if session < 3:
                    print("⏳ 等待2秒後進行下一次測試...")
                    await asyncio.sleep(2)
            
            print("\n🎉 所有測試完成！")
            print("如果每次都能正常啟動和關閉覆蓋層，表示修復成功")
            
        except Exception as e:
            print(f"❌ 測試過程中發生錯誤: {e}")
        finally:
            if self.websocket:
                await self.websocket.close()
    
    async def test_manual_control(self):
        """手動控制測試"""
        if not await self.connect_to_server():
            return
        
        try:
            print("\n" + "="*50)
            print("🎮 手動控制測試模式")
            print("="*50)
            print("輸入命令:")
            print("  lock   - 啟動專注模式")
            print("  unlock - 解除專注模式")
            print("  exit   - 退出測試")
            
            while True:
                command = input("\n請輸入命令: ").strip().lower()
                
                if command == "lock":
                    await self.send_command("lock")
                    print("🔒 已發送啟動命令")
                    
                elif command == "unlock":
                    await self.send_command("unlock")
                    print("🔓 已發送解除命令")
                    
                elif command == "exit":
                    print("👋 退出測試")
                    break
                    
                else:
                    print("❌ 無效命令，請輸入 lock、unlock 或 exit")
                    
        except KeyboardInterrupt:
            print("\n🛑 測試被中斷")
        except Exception as e:
            print(f"❌ 測試錯誤: {e}")
        finally:
            if self.websocket:
                await self.websocket.close()

async def main():
    print("🧪 YouTube 專注模式 - 第二次啟動測試工具")
    print()
    
    tester = FocusModeTester()
    
    while True:
        print("請選擇測試模式:")
        print("1. 自動測試多次啟動")
        print("2. 手動控制測試")
        print("3. 退出")
        
        choice = input("\n請輸入選項 (1-3): ").strip()
        
        if choice == "1":
            await tester.test_multiple_sessions()
        elif choice == "2":
            await tester.test_manual_control()
        elif choice == "3":
            print("👋 測試結束")
            break
        else:
            print("❌ 無效選項")
        
        print("\n" + "-"*40 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
