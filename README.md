# Tavus Shopping Assistant - Chrome Extension

A Chrome extension that embeds a Tavus-powered AI shopping assistant to help users with their shopping experience.

## Project Structure

```
tavus_project/
├── manifest.json           # Extension manifest (Manifest V3)
├── background/
│   └── background.js       # Background service worker
├── content/
│   ├── content.js          # Content script injected into pages
│   └── content.css         # Styles for injected widget
├── popup/
│   ├── popup.html          # Extension popup UI
│   ├── popup.css           # Popup styles
│   └── popup.js            # Popup logic
├── assets/
│   └── icons/              # Extension icons (16, 48, 128px)
└── README.md
```

## How to Load the Extension

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top-right corner)
3. Click "Load unpacked"
4. Select the `tavus_project` folder
5. The extension should now appear in your extensions list

## How to Use

1. Click the extension icon in your Chrome toolbar
2. Click "Activate Assistant" button
3. A widget will appear on the current webpage (bottom-right)
4. You can drag the widget to reposition it
5. Click the X button to close the widget

## Current Features

- ✅ Basic extension structure with Manifest V3
- ✅ Popup interface for activation
- ✅ Content script injection into web pages
- ✅ Draggable assistant widget
- ✅ Background service worker for event handling

## Next Steps

- Add Tavus API integration
- Implement conversation creation
- Add user profile management
- Create settings/options page

## Development Notes

- Uses Manifest V3 (latest Chrome extension standard)
- Organized folder structure for scalability
- Ready for Tavus CVI integration

