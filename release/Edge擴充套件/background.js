// Background script for YouTube Focus Mode
let focusMode = false;
let focusTabId = null;
let focusWindowId = null;
let originalTabId = null;
let preventSwitching = false;

// Listen for tab activation
chrome.tabs.onActivated.addListener((activeInfo) => {
  if (focusMode && activeInfo.tabId !== focusTabId && !preventSwitching) {
    preventSwitching = true;
    
    // Immediately switch back to focus tab
    chrome.tabs.update(focusTabId, { active: true }, () => {
      setTimeout(() => {
        preventSwitching = false;
      }, 100);
    });
    
    // Show notification
    showFocusNotification('請完成YouTube影片觀看後再切換分頁');
  }
});

// Listen for window focus changes
chrome.windows.onFocusChanged.addListener((windowId) => {
  if (focusMode && windowId !== chrome.windows.WINDOW_ID_NONE && windowId !== focusWindowId && !preventSwitching) {
    preventSwitching = true;
    
    // Focus back to the YouTube window and tab
    chrome.tabs.get(focusTabId, (tab) => {
      if (tab && tab.windowId) {
        chrome.windows.update(tab.windowId, { focused: true }, () => {
          chrome.tabs.update(focusTabId, { active: true }, () => {
            setTimeout(() => {
              preventSwitching = false;
            }, 100);
          });
        });
      }
    });
    
    // Show notification
    showFocusNotification('請完成YouTube影片觀看後再切換視窗');
  }
});

// Enhanced window monitoring
let focusCheckInterval = null;

function startFocusMonitoring() {
  if (focusCheckInterval) {
    clearInterval(focusCheckInterval);
  }
  
  focusCheckInterval = setInterval(() => {
    if (!focusMode) {
      clearInterval(focusCheckInterval);
      return;
    }
    
    // Check if focus tab still exists and is active
    chrome.tabs.get(focusTabId, (tab) => {
      if (chrome.runtime.lastError || !tab) {
        // Tab was closed, disable focus mode
        disableFocusMode();
        return;
      }
      
      // Check if the current active tab is our focus tab
      chrome.tabs.query({ active: true, windowId: tab.windowId }, (activeTabs) => {
        if (activeTabs.length > 0 && activeTabs[0].id !== focusTabId && !preventSwitching) {
          preventSwitching = true;
          chrome.tabs.update(focusTabId, { active: true }, () => {
            setTimeout(() => {
              preventSwitching = false;
            }, 100);
          });
        }
      });
      
      // Check if the focused window is correct
      chrome.windows.getCurrent((currentWindow) => {
        if (currentWindow && currentWindow.id !== tab.windowId && !preventSwitching) {
          preventSwitching = true;
          chrome.windows.update(tab.windowId, { focused: true }, () => {
            setTimeout(() => {
              preventSwitching = false;
            }, 100);
          });
        }
      });
    });
  }, 200); // Check every 200ms for more responsive blocking
}

function stopFocusMonitoring() {
  if (focusCheckInterval) {
    clearInterval(focusCheckInterval);
    focusCheckInterval = null;
  }
}

function showFocusNotification(message) {
  chrome.notifications.create({
    type: 'basic',
    iconUrl: 'icons/icon48.png',
    title: '🎯 專注模式已啟用',
    message: message
  });
}

function disableFocusMode() {
  focusMode = false;
  focusTabId = null;
  focusWindowId = null;
  stopFocusMonitoring();
  
  // Update extension icon
  chrome.action.setBadgeText({ text: '' });
  
  // Notify content script
  chrome.tabs.query({url: "*://*.youtube.com/*"}, (tabs) => {
    tabs.forEach(tab => {
      chrome.tabs.sendMessage(tab.id, {
        action: 'focusModeDisabled'
      });
    });
  });
}

// Listen for messages from content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  switch (request.action) {
    case 'enableFocusMode':
      focusMode = true;
      focusTabId = sender.tab.id;
      focusWindowId = sender.tab.windowId;
      originalTabId = sender.tab.id;
      
      // Start intensive monitoring
      startFocusMonitoring();
      
      // Update extension icon
      chrome.action.setBadgeText({ text: 'ON', tabId: focusTabId });
      chrome.action.setBadgeBackgroundColor({ color: '#FF0000' });
      
      // Show activation notification
      showFocusNotification('專注模式已啟用！無法切換視窗直到影片播放完畢');
      
      sendResponse({ success: true });
      break;
      
    case 'disableFocusMode':
      disableFocusMode();
      
      // Show completion notification
      chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icons/icon48.png',
        title: '🎯 專注模式結束',
        message: '影片觀看完畢，您現在可以自由切換視窗了！'
      });
      
      sendResponse({ success: true });
      break;
        case 'getFocusStatus':
      sendResponse({ 
        focusMode: focusMode, 
        focusTabId: focusTabId,
        currentTabId: sender.tab.id 
      });
      break;
      
    case 'forceFocus':
      if (focusMode && focusTabId) {
        chrome.tabs.update(focusTabId, { active: true }, () => {
          chrome.tabs.get(focusTabId, (tab) => {
            if (tab) {
              chrome.windows.update(tab.windowId, { focused: true });
            }
          });
        });
      }
      sendResponse({ success: true });
      break;
  }
});

// Handle tab closure
chrome.tabs.onRemoved.addListener((tabId, removeInfo) => {
  if (tabId === focusTabId) {
    disableFocusMode();
  }
});

// Handle window closure
chrome.windows.onRemoved.addListener((windowId) => {
  if (windowId === focusWindowId) {
    disableFocusMode();
  }
});

// Prevent new tab creation during focus mode
chrome.tabs.onCreated.addListener((tab) => {
  if (focusMode && tab.id !== focusTabId && !preventSwitching) {
    preventSwitching = true;
    
    // Close the new tab and focus back to YouTube
    chrome.tabs.remove(tab.id, () => {
      chrome.tabs.update(focusTabId, { active: true }, () => {
        chrome.windows.update(focusWindowId, { focused: true }, () => {
          setTimeout(() => {
            preventSwitching = false;
          }, 100);
        });
      });
    });
    
    showFocusNotification('無法開啟新分頁，請先完成影片觀看');
  }
});

// Additional security: Monitor keyboard shortcuts
chrome.commands.onCommand.addListener((command) => {
  if (focusMode && (command === 'new-tab' || command === 'new-window')) {
    showFocusNotification('快捷鍵已被阻止，請先完成影片觀看');
  }
});

// Add permission for notifications
chrome.runtime.onStartup.addListener(() => {
  chrome.notifications.getPermissionLevel((level) => {
    if (level !== 'granted') {
      chrome.notifications.getPermissionLevel();
    }
  });
});
