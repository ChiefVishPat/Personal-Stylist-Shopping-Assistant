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
    activateBtn.textContent = 'Creating...';
    info.textContent = 'Creating conversation with assistant...';
    info.style.color = 'white';

    // Get current tab info
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    const pageContext = {
      url: tab.url,
      merchant: extractMerchant(tab.url),
      timestamp: new Date().toISOString()
    };

    console.log('Creating conversation with context:', pageContext);

    // Create Tavus conversation via backend
    const response = await fetch(`${BACKEND_URL}/api/create-conversation`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(pageContext)
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `Backend returned ${response.status}`);
    }

    const data = await response.json();
    console.log('Backend response:', data);

    if (data.success && data.conversation_url) {
      // Try to send message to content script first
      chrome.tabs.sendMessage(tab.id, {
        action: 'showAssistant',
        conversationUrl: data.conversation_url
      }, (response) => {
        if (chrome.runtime.lastError) {
          console.log('Content script not ready, injecting widget directly:', chrome.runtime.lastError.message);
          // Fallback: inject widget directly
          injectWidgetDirectly(tab.id, data.conversation_url);
        } else {
          console.log('Message sent successfully to content script');
        }
      });
      
      // Show success and close popup
      activateBtn.disabled = false;
      activateBtn.textContent = '✓ Ready!';
      info.textContent = 'Assistant is ready!';
      info.style.color = '#90EE90';
      
      // Close popup after short delay
      setTimeout(() => window.close(), 1000);
    } else {
      throw new Error(data.error || data.message || 'Failed to create conversation');
    }

  } catch (error) {
    console.error('Error creating conversation:', error);
    
    // Show error
    activateBtn.disabled = false;
    activateBtn.textContent = 'Retry';
    info.textContent = `Error: ${error.message}. Check backend and API key.`;
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

/**
 * Fallback: Inject widget directly if content script communication fails
 */
function injectWidgetDirectly(tabId, conversationUrl) {
  // Inject CSS first
  chrome.scripting.insertCSS({
    target: { tabId: tabId },
    files: ['content/content.css']
  }).catch(err => console.log('CSS may already be injected:', err));
  
  // Inject widget code
  chrome.scripting.executeScript({
    target: { tabId: tabId },
    func: function(url) {
      // Check if widget already exists
      let container = document.getElementById('tavus-assistant-container');
      if (container) {
        const iframe = container.querySelector('#tavus-conversation-iframe');
        if (iframe) {
          iframe.src = url;
        }
        container.style.display = 'flex';
        return;
      }
      
      // Create widget HTML
      container = document.createElement('div');
      container.id = 'tavus-assistant-container';
      
      container.innerHTML = `
        <div class="tavus-assistant-widget">
          <div class="tavus-header">
            <span class="tavus-title">Shopping Assistant</span>
            <button class="tavus-close" id="tavus-close-btn">×</button>
          </div>
          <div class="tavus-body">
            <iframe id="tavus-conversation-iframe" src="${url}" allow="camera; microphone; fullscreen; display-capture"></iframe>
          </div>
        </div>
      `;
      
      document.body.appendChild(container);
      
      // Add close button handler
      document.getElementById('tavus-close-btn').addEventListener('click', function() {
        container.style.display = 'none';
      });
      
      console.log('Widget injected directly with conversation URL:', url);
    },
    args: [conversationUrl]
  }).catch(error => {
    console.error('Error injecting widget directly:', error);
  });
}
