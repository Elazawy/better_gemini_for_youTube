# Agent Instructions

## Repository Overview
- **Type:** Vanilla JavaScript Chrome Extension (Manifest V3).
- **Purpose:** Resizes the Gemini AI window and text on `youtube.com`.
- **Toolchain:** No build step, no Node.js, no npm, no bundler. All files are used exactly as written.

## Development Workflow
- **Editing:** Modify `content.js`, `styles.css`, `popup.js`, or `popup.html` directly. Do not attempt to use `npm install` or add dependencies.
- **Testing Changes:** 
  1. Open Chrome/Chromium and navigate to `chrome://extensions/`.
  2. If not installed, enable "Developer mode" and click "Load unpacked", selecting this repository folder.
  3. **Crucial:** After making changes to any file, you must click the **Reload** icon (↻) on the extension's card in `chrome://extensions/`.
  4. Refresh the active YouTube tab for the updated `content.js` and `styles.css` to take effect.

## Architecture & Code Conventions
- **`content.js`**: Injected into YouTube pages. Runs as an IIFE to avoid polluting the global scope. Uses DOM observers and polling to find the Gemini UI via CSS selectors. 
  - *Note:* YouTube frequently obfuscates and updates its DOM. If the extension stops working, the selectors in `findGeminiContainer()` are the most likely culprit and will need updating.
- **`styles.css`**: Injected styles for the resize handles and font controls.
- **State/Storage**: Uses `chrome.storage.local` to persist user preferences (width, height, font size) across sessions.
- **Style:** Stick to vanilla DOM manipulation, standard CSS, and standard Chrome Extension APIs.