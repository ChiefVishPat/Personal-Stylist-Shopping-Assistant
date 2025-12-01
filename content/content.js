// Content script - injected into web pages to show the Tavus assistant

console.log('Tavus Shopping Assistant - Content script loaded');

let assistantActive = false;
let assistantContainer = null;

// Listen for messages from background script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'showAssistant') {
    console.log('Received showAssistant message');
    toggleAssistant();
  }
  
  return true;
});

// Toggle assistant visibility
function toggleAssistant() {
  if (assistantActive) {
    hideAssistant();
  } else {
    showAssistant();
  }
}

// Show the assistant widget
function showAssistant() {
  if (assistantContainer) {
    assistantContainer.style.display = 'flex';
    assistantActive = true;
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
        <p class="tavus-placeholder">Assistant will appear here</p>
        <p class="tavus-status">Ready to help you shop!</p>
      </div>
    </div>
  `;
  
  document.body.appendChild(assistantContainer);
  assistantActive = true;
  
  // Add event listeners
  document.getElementById('tavus-close-btn').addEventListener('click', hideAssistant);
  
  // Make widget draggable
  makeDraggable(assistantContainer.querySelector('.tavus-assistant-widget'));
  
  console.log('Assistant widget shown');
}

// Hide the assistant widget
function hideAssistant() {
  if (assistantContainer) {
    assistantContainer.style.display = 'none';
    assistantActive = false;
    console.log('Assistant widget hidden');
  }
}

// Make widget draggable
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
    element.style.top = (element.offsetTop - pos2) + "px";
    element.style.left = (element.offsetLeft - pos1) + "px";
  }

  function closeDragElement() {
    document.onmouseup = null;
    document.onmousemove = null;
  }
}

