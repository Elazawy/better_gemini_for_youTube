import re

with open('content.js', 'r') as f:
    content = f.read()

new_logic = """  // Added by patch
  function addCopyButtons() {
    if (!geminiContainer) return;
    
    // Target the main message renderers in YouTube's AI assistant panel
    const messageBlocks = geminiContainer.querySelectorAll(
      'ytd-ai-assistant-message-renderer, ' +
      'ytd-conversational-item-renderer, ' +
      'yt-formatted-string.ytd-ai-assistant-message-renderer, ' +
      '.markdown-body, ' +
      '[class*="ai-assistant-message"], ' +
      'ytd-engagement-panel-section-list-renderer [role="listitem"] > div'
    );
    
    messageBlocks.forEach(block => {
      // Don't add if already there
      if (block.querySelector(".gemini-copy-btn")) return;
      
      // Skip user messages (often have right alignment or specific user classes/attributes)
      if (block.hasAttribute('is-user-message') || block.tagName === 'YTD-AI-ASSISTANT-USER-MESSAGE-RENDERER') return;
      if (block.className && typeof block.className === 'string' && block.className.includes('user')) return;
      
      // Skip empty or tiny blocks
      if (!block.textContent || block.textContent.trim().length < 15) return;
      
      // Skip input areas and buttons
      if (block.tagName === 'INPUT' || block.tagName === 'TEXTAREA' || block.hasAttribute('contenteditable')) return;
      if (block.tagName === 'BUTTON' || block.closest('button')) return;
      if (block.tagName === 'YTD-BUTTON-RENDERER' || block.closest('ytd-button-renderer')) return;
      
      // We want to attach the button to the bottom of the text. 
      // Sometimes block is a container, sometimes it's the text itself.
      const btnContainer = document.createElement("div");
      btnContainer.className = "gemini-copy-container";
      btnContainer.style.marginTop = "8px";
      btnContainer.style.marginBottom = "8px";
      btnContainer.style.display = "flex";
      btnContainer.style.justifyContent = "flex-end"; // Align right (or left in RTL, flex-end adapts)
      btnContainer.style.width = "100%";
      
      const btn = document.createElement("button");
      btn.className = "gemini-copy-btn";
      btn.innerHTML = "📋 Copy";
      btn.title = "Copy response to clipboard";
      btn.style.cssText = `
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 6px 12px;
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        color: var(--yt-spec-text-primary, inherit);
        font-size: 13px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
        font-family: inherit;
        z-index: 10;
      `;
      
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        e.preventDefault();
        
        // Try to find the actual text content container within this block to avoid copying buttons
        let textNode = block;
        const formattedString = block.querySelector('yt-formatted-string');
        const markdownBody = block.querySelector('.markdown-body');
        
        if (markdownBody) {
            textNode = markdownBody;
        } else if (formattedString) {
            textNode = formattedString;
        }
        
        const clone = textNode.cloneNode(true);
        
        // Clean up the clone
        const toRemove = clone.querySelectorAll('.gemini-copy-container, .gemini-text-controls, button, ytd-button-renderer, yt-icon-button, [role="button"]');
        toRemove.forEach(el => el.remove());
        
        const textToCopy = (clone.innerText || clone.textContent).trim();
        
        if (!textToCopy) return;
        
        navigator.clipboard.writeText(textToCopy).then(() => {
          btn.innerHTML = "✅ Copied!";
          btn.style.background = "rgba(0, 150, 136, 0.2)";
          btn.style.borderColor = "rgba(0, 150, 136, 0.5)";
          setTimeout(() => {
            btn.innerHTML = "📋 Copy";
            btn.style.background = "rgba(255, 255, 255, 0.1)";
            btn.style.borderColor = "rgba(255, 255, 255, 0.2)";
          }, 2000);
        }).catch(err => {
          console.error("Failed to copy text: ", err);
          btn.innerHTML = "❌ Failed";
        });
      });
      
      btn.addEventListener("mouseenter", () => {
          if(btn.innerHTML === "📋 Copy") {
              btn.style.background = "rgba(255, 255, 255, 0.2)";
          }
      });
      btn.addEventListener("mouseleave", () => {
        if(btn.innerHTML === "📋 Copy") {
            btn.style.background = "rgba(255, 255, 255, 0.1)";
        }
      });
      
      btnContainer.appendChild(btn);
      
      // Look for the action bar (thumbs up/down) to insert near it if possible
      const actionBar = block.querySelector('#action-buttons, .action-buttons, ytd-ai-assistant-message-action-renderer, [id="feedback-buttons"]');
      
      if (actionBar && actionBar.parentNode) {
          actionBar.parentNode.insertBefore(btnContainer, actionBar.nextSibling);
      } else {
          block.appendChild(btnContainer);
      }
    });
  }"""

# Replace the old function definition
content = re.sub(r'  // Added by patch\n  function addCopyButtons\(\) \{[\s\S]*?    \}\);\n  \}', new_logic, content)

with open('content.js', 'w') as f:
    f.write(content)
