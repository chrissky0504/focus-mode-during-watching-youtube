## Language / 語言
- [中文版 README](README.md)
- [English README](README_EN.md) (Current)

# YouTube Focus Mode Edge Extension

This is a system that helps users focus on watching YouTube videos, combining an Edge browser extension with a local Python program.

## System Components

### Edge Extension
- `manifest.json` - Extension configuration
- `content.js` - YouTube page script
- `background.js` - Background service
- `popup.html/js` - Popup interface
- `options.html/js` - Settings page

### Python Backend
- `screen_blocker_final_fixed.py` - **Main Program** (Latest version with complete fixes)
- `super_fix_topmost.py` - Emergency repair tool
- `test_second_start.py` - Test tool for multiple starts

## Quick Installation

### 1. Download Installation Package
```bash
git clone https://github.com/chrissky0504/focus-mode-during-watching-youtube.git
cd focus-mode-during-watching-youtube
```

### 2. Install Python Dependencies
```bash
pip install websockets pywin32
```

### 3. Install Edge Extension
1. Open Edge browser
2. Go to `edge://extensions/`
3. Enable "Developer mode"
4. Click "Load unpacked"
5. Select the `focus` folder of this project

## How to Use

### 1. Start Backend Program
```bash
# Start main program
python screen_blocker_final_fixed.py

# Or use the launcher
start_final_fixed.bat
```

### 2. Use Focus Mode
1. Open a YouTube video
2. Click the Focus Mode icon in Edge toolbar
3. Click "Start Focus Mode" button
4. The system will automatically:
   - 🔒 Create screen edge overlay layers
   - 📌 Set Edge window to always on top
   - 🚫 Block all click behaviors that switch windows

### 3. End Focus Mode
Focus mode will automatically end in the following situations:
- ✅ YouTube video playback completes

The system will automatically:
- 📌 Cancel Edge window topmost status
- 🔓 Remove screen overlay layers
- 💬 Display end notification

## Test Tools

### Multiple Start Test
```bash
python test_second_start.py
```
This tool will:
1. Test multiple focus mode starts/stops
2. Verify overlay layers can be recreated properly
3. Provide manual control testing

### Emergency Repair Tool
If windows get stuck in topmost state:
```bash
python super_fix_topmost.py    # Remove all topmost windows
```

## Overlay Area Configuration

screen_blocker_final_fixed.py overlay settings:
- **Top**: 60px height, blocks clicking other window title bars
- **Bottom**: 60px height, blocks clicking taskbar
- **Left**: 60px width, blocks left-side operations
- **Right**: 600px width, effectively blocks window switching gestures

## Troubleshooting

### Common Issues

1. **Cannot find Edge windows**
   - Ensure Edge browser is open
   - Ensure YouTube or any webpage is open
   - Check if using correct Edge version (not IE mode)

2. **Windows cannot be set to topmost**
   - Run Python program as administrator
   - Check for conflicts with other software

3. **Dependency installation failed**
   - Ensure Python version 3.7+
   - Try upgrading pip: `python -m pip install --upgrade pip`
   - Manual installation: `pip install websockets pywin32`

4. **Second start fails**
   - This has been fixed in the latest version
   - Use `screen_blocker_final_fixed.py`

### System Requirements
- Windows 10/11
- Python 3.7+
- Microsoft Edge browser
- Internet connection (for dependency installation)

## Development Information

### File Structure
```
focus/
├── manifest.json                    # Extension configuration
├── content.js                       # YouTube page script
├── background.js                    # Background service
├── popup.html/js                    # Popup window
├── options.html/js                  # Settings page
├── styles.css                       # Stylesheet
├── screen_blocker_final_fixed.py    # Main program ⭐
├── super_fix_topmost.py             # Emergency repair tool
├── test_second_start.py             # Test tool
└── start_final_fixed.bat            # Launcher
```

### Communication Protocol
Extension and Python program communicate via WebSocket (localhost:8080):

```json
{
  "action": "lock",        // Start focus mode
  "action": "unlock",      // End focus mode  
  "action": "progress",    // Video progress update
  "progress": 75.5         // Progress percentage
}
```

## Update Log

### Final Fixed Version (Latest)
- 🆕 Complete fix for second start issues
- 🆕 Enhanced state reset mechanism
- 🆕 Improved window creation with proper parent-child relationships
- 🆕 Thread-safe monitoring system
- 🔧 Fixed overlay layers not disappearing after video ends
- 🔧 Fixed overlay layers disappearing in fullscreen mode
- 🔧 Enhanced error handling and user feedback

### v3.0
- 🆕 Added Edge window auto topmost/cancel topmost functionality
- 🆕 Smart detection of all Edge browser windows
- 🆕 Right overlay layer widened to 550px
- 🔧 Fixed fullscreen mode click-through issues
- 🔧 Improved error handling and user notifications

### v2.0
- Added screen edge overlay functionality
- Fixed various window management issues
- Improved WebSocket communication stability

### v1.0
- Basic focus mode functionality
- Edge extension development
- YouTube video progress detection

---

🎯 **Focus Mode helps you fully immerse in YouTube learning!**

