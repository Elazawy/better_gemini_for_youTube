// Popup script for YouTube Gemini Resizer

document.addEventListener('DOMContentLoaded', async () => {
  const decreaseBtn = document.getElementById('decreaseBtn');
  const increaseBtn = document.getElementById('increaseBtn');
  const resetBtn = document.getElementById('resetBtn');
  const sizeDisplay = document.getElementById('sizeDisplay');

  // Get current tab
  async function getCurrentTab() {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    return tab;
  }

  // Send message to content script
  async function sendMessage(action, data = {}) {
    try {
      const tab = await getCurrentTab();
      if (tab?.id) {
        await chrome.tabs.sendMessage(tab.id, { action, ...data });
      }
    } catch (e) {
      console.error('Failed to send message:', e);
    }
  }

  // Update size display
  async function updateSizeDisplay() {
    try {
      const tab = await getCurrentTab();
      if (tab?.id) {
        const response = await chrome.tabs.sendMessage(tab.id, { action: 'getSettings' });
        if (response?.fontSize) {
          sizeDisplay.textContent = `${response.fontSize}px`;
        }
      }
    } catch (e) {
      // Default value if we can't get settings
      sizeDisplay.textContent = '14px';
    }
  }

  // Decrease text size
  decreaseBtn.addEventListener('click', async () => {
    await sendMessage('adjustTextSize', { delta: -2 });
    await updateSizeDisplay();
  });

  // Increase text size
  increaseBtn.addEventListener('click', async () => {
    await sendMessage('adjustTextSize', { delta: 2 });
    await updateSizeDisplay();
  });

  // Reset to defaults
  resetBtn.addEventListener('click', async () => {
    await sendMessage('resetSize');
    sizeDisplay.textContent = '14px';
  });

  // Initialize
  await updateSizeDisplay();
});