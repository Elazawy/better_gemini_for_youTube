# YouTube Gemini Resizer

A Chrome extension that allows you to resize the Gemini AI window and text on YouTube.

## Features

- **Resize Window**: Drag the right, bottom, or corner resize handle to adjust the Gemini AI window size
- **Text Size Control**: Increase or decrease text size with A+/A- buttons
- **Persistent Settings**: Your preferred window size and text size are saved
- **Dark Mode Support**: Works with YouTube's dark theme

## Installation

### Method 1: Load Unpacked (Developer Mode)

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable **Developer mode** (toggle in top right corner)
3. Click **Load unpacked**
4. Select this folder (`resize-youtube-ai`)
5. The extension is now installed!

### Method 2: From Chrome Web Store (when published)

Coming soon...

## Usage

1. Go to YouTube and open any video
2. Click the **Gemini** button (usually appears at the bottom of the video)
3. The Gemini AI window will appear with resize handles:
   - **Right edge handle**: Drag horizontally to adjust width only
   - **Bottom edge handle**: Drag vertically to adjust height only
   - **Corner handle**: Drag diagonally to adjust both width and height

4. Use the text size controls at the top of the Gemini window:
   - **A-**: Decrease text size
   - **A+**: Increase text size

5. Click the extension icon in the toolbar for quick text size adjustments

## File Structure

```
resize-youtube-ai/
├── manifest.json      # Extension configuration
├── content.js         # Main script that adds resize functionality
├── styles.css         # Styles for resize handles and controls
├── popup.html         # Extension popup UI
├── popup.js           # Popup script
├── icon16.png         # Extension icon (16x16)
├── icon48.png         # Extension icon (48x48)
├── icon128.png        # Extension icon (128x128)
└── README.md          # This file
```

## How It Works

The extension injects a content script into YouTube pages that:

1. Detects when the Gemini AI sidebar/window appears
2. Adds resize handles (right, bottom, corner) to the container
3. Adds text size controls (A-/A+ buttons) to the UI
4. Persists user preferences using Chrome storage API
5. Automatically applies saved settings when Gemini opens

## Customization

### Change Default Size

Edit the `DEFAULTS` object in `content.js`:

```javascript
const DEFAULTS = {
  width: 400,    // Change default width
  height: 600,   // Change default height
  fontSize: 14,  // Change default font size
  position: 'right'
};
```

### Change Resize Handle Color

Edit the CSS in `styles.css`. Look for color values like `#4285f4` (Google Blue).

## Troubleshooting

**Extension not working?**

1. Make sure you're on a YouTube video page
2. Check that the Gemini AI button is visible
3. Try refreshing the page
4. Check the browser console for errors (F12 → Console)

**Resize handles not appearing?**

1. The Gemini container might have a different selector
2. Check the console for "YouTube Gemini Resizer: Extension loaded"
3. Try clicking the Gemini button again

**Text size not changing?**

Some elements in the Gemini UI might have inline styles. The extension applies `!important` to override most cases.

## Browser Compatibility

- Chrome 88+ (Manifest V3)
- Edge 88+ (Chromium-based)
- Other Chromium-based browsers supporting Manifest V3

## Privacy

This extension:
- ✅ Only runs on YouTube pages (`https://www.youtube.com/*`)
- ✅ Stores settings locally in your browser
- ✅ Does not collect any personal data
- ✅ Does not send data to external servers

## License

MIT License - Feel free to modify and distribute!

## Contributing

Pull requests are welcome! For major changes, please open an issue first.

## Changelog

### v1.0.0
- Initial release
- Resize handles for Gemini AI window
- Text size adjustment controls
- Persistent settings storage
- Dark mode support
