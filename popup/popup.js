// Popup script - handles user interactions in the extension popup

document.addEventListener('DOMContentLoaded', () => {
  const activateBtn = document.getElementById('activateBtn');
  const settingsLink = document.getElementById('settingsLink');

  // Handle activate button click
  activateBtn.addEventListener('click', async () => {
    // Get the active tab
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    // Send message to background script to activate assistant
    chrome.runtime.sendMessage({
      action: 'activateAssistant',
      tabId: tab.id
    });
    
    // Visual feedback
    activateBtn.textContent = 'Activating...';
    setTimeout(() => {
      activateBtn.textContent = 'Activate Assistant';
      window.close(); // Close popup after activation
    }, 500);
  });

  // Handle settings link click
  settingsLink.addEventListener('click', (e) => {
    e.preventDefault();
    // TODO: Open settings page when created
    chrome.runtime.openOptionsPage();
  });
});

