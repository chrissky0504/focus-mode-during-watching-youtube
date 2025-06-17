// Content script for YouTube Focus Mode
let focusButton = null;
let isInFocusMode = false;
let videoElement = null;
let progressCheckInterval = null;
let socket = null;

// Initialize when page loads
function init() {
  // Wait for YouTube player to load
  setTimeout(() => {
    findVideoElement();
    createFocusButton();
    setupVideoEventListeners();
  }, 2000);
}

// Find the video element on the page
function findVideoElement() {
  videoElement = document.querySelector('video');
  if (!videoElement) {
    // Retry after a short delay if video not found
    setTimeout(findVideoElement, 1000);
  }
}

// Create the focus mode button
function createFocusButton() {
  if (focusButton || !document.querySelector('.ytp-chrome-bottom')) {
    return;
  }
  
  focusButton = document.createElement('button');
  focusButton.innerHTML = '🎯 專注模式';
  focusButton.className = 'focus-mode-btn';
  focusButton.id = 'youtube-focus-btn';
  
  // Add button styles
  focusButton.style.cssText = `
    position: absolute;
    top: 10px;
    right: 10px;
    z-index: 9999;
    background: #ff0000;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-size: 14px;
    cursor: pointer;
    font-weight: bold;
    box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    transition: all 0.3s ease;
  `;
  
  focusButton.addEventListener('click', toggleFocusMode);
  focusButton.addEventListener('mouseenter', () => {
    focusButton.style.background = '#cc0000';
  });
  focusButton.addEventListener('mouseleave', () => {
    focusButton.style.background = isInFocusMode ? '#00cc00' : '#ff0000';
  });
  
  // Add button to the player
  const playerContainer = document.querySelector('#movie_player') || document.querySelector('.html5-video-player');
  if (playerContainer) {
    playerContainer.appendChild(focusButton);
  }
}

// Toggle focus mode
function toggleFocusMode() {
  if (!videoElement) {
    alert('找不到影片元素，請重新整理頁面');
    return;
  }
  
  if (isInFocusMode) {
    disableFocusMode();
  } else {
    enableFocusMode();
  }
}

// Enable focus mode
function enableFocusMode() {
  if (!videoElement || videoElement.paused) {
    alert('請先播放影片再啟用專注模式');
    return;
  }
  
  isInFocusMode = true;
  focusButton.innerHTML = '✅ 專注中';
  focusButton.style.background = '#00cc00';  
  // Send message to background script
  chrome.runtime.sendMessage({ action: 'enableFocusMode' });
  
  // Send lock signal to Python server
  sendLockSignalToServer();
  
  // Start monitoring video progress
  startProgressMonitoring();
  
  // Note: Focus overlay disabled for cleaner experience
  // showFocusOverlay();
}

// Disable focus mode
function disableFocusMode() {
  isInFocusMode = false;
  focusButton.innerHTML = '🎯 專注模式';
  focusButton.style.background = '#ff0000';
  
  // Send message to background script
  chrome.runtime.sendMessage({ action: 'disableFocusMode' });
  
  // Send unlock signal to Python server
  sendUnlockSignalToServer();
  
  // Stop monitoring
  if (progressCheckInterval) {
    clearInterval(progressCheckInterval);
    progressCheckInterval = null;
  }  
  // Note: Focus overlay disabled for cleaner experience
  // hideFocusOverlay();
}

// Connect to WebSocket server
function connectWebSocket() {
  socket = new WebSocket('ws://localhost:8080');

  socket.onopen = () => {
    console.log('WebSocket連線成功');
  };

  socket.onerror = (error) => {
    console.error('WebSocket錯誤:', error);
  };

  socket.onclose = () => {
    console.log('WebSocket連線已關閉');
    setTimeout(connectWebSocket, 5000); // 重試連線
  };
}

// Send video progress to WebSocket server
function sendProgressToServer(progress) {
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify({ action: 'progress', progress }));
  }
}

// Send lock signal to Python server
function sendLockSignalToServer() {
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify({ action: 'lock' }));
    console.log('已發送鎖定訊號到Python伺服器');
  }
}

// Send unlock signal to Python server
function sendUnlockSignalToServer() {
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify({ action: 'unlock' }));
    console.log('已發送解鎖訊號到Python伺服器');
  }
}

// Monitor video progress
function startProgressMonitoring() {
  progressCheckInterval = setInterval(() => {
    if (!videoElement || !isInFocusMode) {
      clearInterval(progressCheckInterval);
      return;
    }
      // Check if video ended or reached the end
    if (videoElement.ended || 
        (videoElement.duration > 0 && 
         Math.abs(videoElement.currentTime - videoElement.duration) < 1)) {
      disableFocusMode();
    }
    
    // Progress indicator disabled for cleaner experience
    // updateProgressIndicator();

    // Send progress to server
    const progress = (videoElement.currentTime / videoElement.duration) * 100;
    sendProgressToServer(progress);
  }, 1000);
}

// Update progress indicator (disabled for cleaner experience)
function updateProgressIndicator() {
  // Progress indicator disabled - no UI elements shown
  return;
}

// Show focus mode overlay
function showFocusOverlay() {
  const overlay = document.createElement('div');
  overlay.id = 'focus-mode-overlay';
  overlay.innerHTML = `
    <div class="focus-info">
      <h3>🎯 專注模式已啟用</h3>
      <p id="focus-progress-text">正在監控影片進度...</p>
      <div class="focus-progress-bar">
        <div id="focus-progress-indicator"></div>
      </div>
      <p class="focus-note">影片播放完畢前無法切換視窗</p>
    </div>
  `;
  
  overlay.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    z-index: 10000;
    padding: 10px;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    animation: slideDown 0.5s ease;
  `;
  
  document.body.appendChild(overlay);
}

// Hide focus mode overlay
function hideFocusOverlay() {
  const overlay = document.getElementById('focus-mode-overlay');
  if (overlay) {
    overlay.style.animation = 'slideUp 0.5s ease';
    setTimeout(() => {
      overlay.remove();
    }, 500);
  }
}

// Setup video event listeners
function setupVideoEventListeners() {
  if (!videoElement) return;
  
  videoElement.addEventListener('ended', () => {
    if (isInFocusMode) {
      disableFocusMode();
    }
  });
  
  videoElement.addEventListener('pause', () => {
    if (isInFocusMode) {
      // Optionally disable focus mode when video is paused
      // disableFocusMode();
    }
  });
}

// Handle navigation changes (for single page app)
function handleNavigation() {
  // Reset state on navigation
  isInFocusMode = false;
  focusButton = null;
  videoElement = null;
  
  if (progressCheckInterval) {
    clearInterval(progressCheckInterval);
    progressCheckInterval = null;
  }
  
  // Reinitialize after navigation
  setTimeout(init, 1000);
}

// Listen for YouTube navigation
let lastUrl = location.href;
new MutationObserver(() => {
  const url = location.href;
  if (url !== lastUrl) {
    lastUrl = url;
    handleNavigation();
  }
}).observe(document, { subtree: true, childList: true });

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}

// Handle page visibility change
document.addEventListener('visibilitychange', () => {
  if (document.hidden && isInFocusMode) {
    // Page is hidden but we're in focus mode - prevent this
    setTimeout(() => {
      if (document.hidden && isInFocusMode) {
        window.focus();
        // Try to bring window to front
        if (window.chrome && window.chrome.runtime) {
          chrome.runtime.sendMessage({
            action: 'forceFocus'
          });
        }
      }
    }, 50);
  }
});

// Prevent common escape methods
document.addEventListener('keydown', (e) => {
  if (isInFocusMode) {
    // Prevent Alt+Tab, Ctrl+Tab, Ctrl+W, Ctrl+T, etc.
    if ((e.altKey && e.key === 'Tab') ||
        (e.ctrlKey && (e.key === 'Tab' || e.key === 'w' || e.key === 't' || 
                       e.key === 'n' || e.key === '1' || e.key === '2' || 
                       e.key === '3' || e.key === '4' || e.key === '5' || 
                       e.key === '6' || e.key === '7' || e.key === '8' || 
                       e.key === '9'))) {
      e.preventDefault();
      e.stopPropagation();
      
      // Show warning
      showTemporaryWarning('快捷鍵已被阻止！請完成影片觀看');
      return false;
    }
    
    // Prevent F11 (fullscreen toggle that might allow escape)
    if (e.key === 'F11') {
      e.preventDefault();
      showTemporaryWarning('全螢幕切換已被阻止！請完成影片觀看');
      return false;
    }
  }
}, true);

// Prevent right-click context menu during focus mode
document.addEventListener('contextmenu', (e) => {
  if (isInFocusMode) {
    e.preventDefault();
    showTemporaryWarning('右鍵選單已被阻止！請完成影片觀看');
    return false;
  }
}, true);

// Function to show temporary warning
function showTemporaryWarning(message) {
  const warning = document.createElement('div');
  warning.textContent = message;
  warning.style.cssText = `
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: rgba(255, 0, 0, 0.9);
    color: white;
    padding: 20px 40px;
    border-radius: 10px;
    font-size: 16px;
    font-weight: bold;
    z-index: 999999;
    box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    border: 2px solid #ff4444;
  `;
  
  document.body.appendChild(warning);
  
  setTimeout(() => {
    if (warning.parentNode) {
      warning.remove();
    }
  }, 2000);
}

// Listen for messages from background script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'focusModeDisabled') {
    if (isInFocusMode) {
      disableFocusMode();
    }
  }
});

connectWebSocket();
