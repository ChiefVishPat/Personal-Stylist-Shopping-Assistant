// Popup script - handles extension popup interactions

const BACKEND_URL = 'http://localhost:8000';

document.addEventListener('DOMContentLoaded', () => {
  const activateBtn = document.getElementById('activateBtn');
  const info = document.querySelector('.info p');

  // Check backend connection when popup opens
  checkBackendConnection();

  activateBtn.addEventListener('click', async () => {
    await sendPageContext();
  });
});

async function checkBackendConnection() {
  try {
    // Check if backend is reachable
    const response = await fetch(`${BACKEND_URL}/`, {
      method: 'GET'
    });

    if (!response.ok) {
      throw new Error(`Backend returned ${response.status}`);
    }

    console.log('Backend is reachable');
  } catch (error) {
    console.error('Backend connection error:', error);
  }
}

async function sendPageContext() {
  const activateBtn = document.getElementById('activateBtn');
  const info = document.querySelector('.info p');

  try {
    // Show loading
    activateBtn.disabled = true;
    activateBtn.textContent = 'Sending...';
    info.textContent = 'Sending page context to backend...';
    info.style.color = 'white';

    // Get current tab info
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    const pageContext = {
      url: tab.url,
      merchant: extractMerchant(tab.url),
      timestamp: new Date().toISOString()
    };

    console.log('Sending page context:', pageContext);

    // Send page context to backend
    const response = await fetch(`${BACKEND_URL}/api/page-context`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(pageContext)
    });

    if (!response.ok) {
      throw new Error(`Backend returned ${response.status}`);
    }

    const data = await response.json();
    console.log('Backend response:', data);

    // Show success
    activateBtn.disabled = false;
    activateBtn.textContent = 'Sent!';
    info.textContent = data.message || 'Context sent successfully';
    info.style.color = '#90EE90';

  } catch (error) {
    console.error('Error sending page context:', error);
    
    // Show error
    activateBtn.disabled = false;
    activateBtn.textContent = 'Retry';
    info.textContent = `Error: ${error.message}. Is backend running?`;
    info.style.color = '#ff6b6b';
  }
}

function extractMerchant(url) {
  try {
    const hostname = new URL(url).hostname;
    const parts = hostname.split('.');
    // Get domain name (e.g., "uniqlo" from "www.uniqlo.com")
    const domain = parts.length >= 2 ? parts[parts.length - 2] : hostname;
    return domain.charAt(0).toUpperCase() + domain.slice(1);
  } catch {
    return 'Unknown';
  }
}
