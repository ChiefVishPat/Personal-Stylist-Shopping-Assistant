// Background service worker - handles extension events and API calls

console.log('Tavus Shopping Assistant - Background service worker loaded');

// Listen for messages from popup or content scripts
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'activateAssistant') {
    console.log('Activating assistant for tab:', message.tabId);
    
    // Inject content script or send message to existing one
    chrome.tabs.sendMessage(message.tabId, {
      action: 'showAssistant'
    }).catch(error => {
      console.log('Content script not ready, will be injected automatically');
    });
  }
  
  return true; // Keep message channel open for async responses
});

// Listen for extension icon clicks (alternative activation method)
chrome.action.onClicked.addListener(async (tab) => {
  console.log('Extension icon clicked on tab:', tab.id);
  
  // Send message to content script
  chrome.tabs.sendMessage(tab.id, {
    action: 'showAssistant'
  }).catch(error => {
    console.log('Content script not ready');
  });
});

// Initialize extension storage with default values
chrome.runtime.onInstalled.addListener(() => {
  console.log('Extension installed/updated');
  
  // Set default storage values
  chrome.storage.local.set({
    isActivated: false,
    assistantPosition: { x: 20, y: 20 }
  });
  
  // TODO: Open onboarding page on first install
});

