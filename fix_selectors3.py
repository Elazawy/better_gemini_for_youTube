import re

with open('content.js', 'r') as f:
    content = f.read()

# Add a more aggressive selector to ensure we find the text.
# `ytd-engagement-panel-section-list-renderer` is the whole panel, and `ytd-conversational-item-renderer` is the specific message block.
new_selector_logic = """  // Added by patch
  function addCopyButtons() {
    if (!geminiContainer) return;
    
    // Look for the main AI message containers in YouTube's new AI panel
    const messageBlocks = Array.from(geminiContainer.querySelectorAll(
      'ytd-ai-assistant-core-message-renderer, ' +
      'ytd-conversational-item-renderer, ' +
      'yt-formatted-string.ytd-ai-assistant-message-renderer, ' +
      'div#content.ytd-conversational-item-renderer'
    )).filter(block => {
        // Only get blocks that have the actual bot text, ignore user messages
        return !block.closest('ytd-ai-assistant-user-message-renderer');
    });

    // If those specific AI tags aren't found, try a fallback for standard text blocks inside the panel
    if (messageBlocks.length === 0) {
        const fallbacks = geminiContainer.querySelectorAll('ytd-engagement-panel-section-list-renderer [role="listitem"] > div');
        fallbacks.forEach(f => {
            if (!f.querySelector('img.ytd-ai-assistant-user-message-renderer')) { // skip if it's user
                messageBlocks.push(f);
            }
        });
    }

    messageBlocks.forEach(block => {"""

content = re.sub(r'  // Added by patch\n  function addCopyButtons\(\) \{[\s\S]*?    messageBlocks\.forEach\(block => \{', new_selector_logic, content)

with open('content.js', 'w') as f:
    f.write(content)
