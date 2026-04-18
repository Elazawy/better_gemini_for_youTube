import re

with open('content.js', 'r') as f:
    content = f.read()

# Replace the overly specific selectors with broader ones that catch YouTube's "Ask" AI elements
old_selector_block = """    const messageBlocks = geminiContainer.querySelectorAll(
      '[class*="message-body"], [class*="model-response"], [class*="response-content"], .message-content, [class*="gemini-message"], ytd-engagement-panel-section-list-renderer [role="listitem"] div:not([class*="user"])'
    );"""

new_selector_block = """    // YouTube's native AI chat often uses specific custom elements or generic containers
    const messageBlocks = geminiContainer.querySelectorAll(
      'yt-formatted-string.content, ' + 
      'yt-formatted-string[id="content-text"], ' + 
      '.markdown-body, ' + 
      '[class*="message-body"], ' + 
      '[class*="model-response"], ' + 
      '[class*="response-content"], ' + 
      '.message-content, ' + 
      '[class*="gemini-message"], ' + 
      'ytd-engagement-panel-section-list-renderer [role="listitem"] div:not([class*="user"]), ' +
      'ytd-conversational-item-renderer, ' + 
      'ytd-ai-assistant-message-renderer, ' +
      '[class*="ai-assistant-message"], ' +
      'div[dir="auto"]' // Common for Arabic/RTL auto-detected text containers
    );"""

content = content.replace(old_selector_block, new_selector_block)

# Also remove the avatar check, as it might accidentally block the bot's avatar!
old_avatar_check = """      if (block.querySelector('img[class*="avatar"]')) return;"""
new_avatar_check = """      // Removed avatar check as it might block the bot's own avatar icon
      // if (block.querySelector('img[class*="avatar"]')) return;
      
      // Also skip buttons (like the suggested prompts)
      if (block.tagName === 'BUTTON' || block.closest('button')) return;"""

content = content.replace(old_avatar_check, new_avatar_check)

with open('content.js', 'w') as f:
    f.write(content)
