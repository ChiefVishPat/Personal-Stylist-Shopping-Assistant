// Content script injected into web pages
// Creates and manages the draggable assistant widget with Tavus conversation iframe

console.log('Tavus Shopping Assistant - Content script loaded');

let assistantActive = false;
let assistantContainer = null;
let currentConversationUrl = null;

// Listen for messages from popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'showAssistant' && message.conversationUrl) {
    console.log('Received conversation URL:', message.conversationUrl);
    showAssistant(message.conversationUrl);
    sendResponse({ success: true });
    return true;
  }
  return true;
});

/**
 * Show the assistant widget with Tavus conversation iframe.
 * @param {string} conversationUrl - Tavus conversation URL
 */
function showAssistant(conversationUrl) {
  if (assistantContainer && assistantActive) {
    // Update iframe src if already showing
    const iframe = assistantContainer.querySelector('#tavus-conversation-iframe');
    if (iframe) {
      iframe.src = conversationUrl;
    }
    assistantContainer.style.display = 'flex';
    return;
  }
  
  // Create assistant container
  assistantContainer = document.createElement('div');
  assistantContainer.id = 'tavus-assistant-container';
  assistantContainer.innerHTML = `
    <div class="tavus-assistant-widget">
      <div class="tavus-header">
        <span class="tavus-title">Shopping Assistant</span>
        <button class="tavus-close" id="tavus-close-btn">×</button>
      </div>
      <div class="tavus-body">
        <iframe 
          id="tavus-conversation-iframe"
          src="${conversationUrl}"
          allow="camera; microphone; fullscreen; display-capture"
        ></iframe>
      </div>
    </div>
  `;
  
  document.body.appendChild(assistantContainer);
  assistantActive = true;
  currentConversationUrl = conversationUrl;
  
  // Add event listeners
  document.getElementById('tavus-close-btn').addEventListener('click', hideAssistant);
  
  // Make widget draggable
  makeDraggable(assistantContainer.querySelector('.tavus-assistant-widget'));
  
  console.log('Assistant widget shown with conversation URL');
}

/**
 * Hide the assistant widget.
 */
function hideAssistant() {
  if (assistantContainer) {
    assistantContainer.style.display = 'none';
    assistantActive = false;
    console.log('Assistant widget hidden');
  }
}

/**
 * Make widget draggable by header.
 * @param {HTMLElement} element - The widget element
 */
function makeDraggable(element) {
  let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
  const header = element.querySelector('.tavus-header');
  
  header.style.cursor = 'move';
  header.onmousedown = dragMouseDown;

  function dragMouseDown(e) {
    e.preventDefault();
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.onmouseup = closeDragElement;
    document.onmousemove = elementDrag;
  }

  function elementDrag(e) {
    e.preventDefault();
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;
    const newTop = element.offsetTop - pos2;
    const newLeft = element.offsetLeft - pos1;
    
    // Keep widget within viewport bounds
    const maxTop = window.innerHeight - element.offsetHeight;
    const maxLeft = window.innerWidth - element.offsetWidth;
    
    element.style.top = Math.max(0, Math.min(newTop, maxTop)) + "px";
    element.style.left = Math.max(0, Math.min(newLeft, maxLeft)) + "px";
    element.style.right = 'auto';
    element.style.bottom = 'auto';
  }

  function closeDragElement() {
    document.onmouseup = null;
    document.onmousemove = null;
  }
}
