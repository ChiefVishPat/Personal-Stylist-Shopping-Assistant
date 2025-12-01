// Background service worker
// Handles extension events and message routing

console.log('Tavus Shopping Assistant - Background worker loaded');

// Listen for messages from popup or content scripts
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('Background received message:', message);
  return true;
});
