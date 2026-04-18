import re

with open('content.js', 'r') as f:
    content = f.read()

# Remove the incorrectly placed addCopyButtons() calls
content = re.sub(r'[ \t]*addCopyButtons\(\);\n', '', content)

# Remove the function definition if it exists
content = re.sub(r'  // Added by patch\n  function addCopyButtons\(\) \{[\s\S]*?    \}\);\n  \}\n', '', content)

# Now append it cleanly at the bottom before the IIFE closing
correct_code = """
  // Added by patch
  function addCopyButtons() {
    if (!geminiContainer) return;
    const messageBlocks = geminiContainer.querySelectorAll(
      '[class*="message-body"], [class*="model-response"], [class*="response-content"], .message-content, [class*="gemini-message"], ytd-engagement-panel-section-list-renderer [role="listitem"] div:not([class*="user"])'
    );
    messageBlocks.forEach(block => {
      if (block.querySelector(".gemini-copy-btn")) return;
      if (block.tagName === "INPUT" || block.tagName === "TEXTAREA" || block.hasAttribute("contenteditable")) return;
      if (!block.textContent || block.textContent.trim().length < 5) return;
      if (block.querySelector('img[class*="avatar"]')) return;
      
      const btnContainer = document.createElement("div");
      btnContainer.className = "gemini-copy-container";
      btnContainer.style.marginTop = "8px";
      btnContainer.style.textAlign = "left";
      
      const btn = document.createElement("button");
      btn.className = "gemini-copy-btn";
      btn.innerHTML = "📋 Copy";
      btn.title = "Copy response to clipboard";
      btn.style.cssText = `
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 4px 8px;
        background: rgba(128, 128, 128, 0.2);
        border: 1px solid rgba(128, 128, 128, 0.3);
        border-radius: 4px;
        color: inherit;
        font-size: 12px;
        cursor: pointer;
        transition: all 0.2s;
        font-family: inherit;
      `;
      
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        const clone = block.cloneNode(true);
        const container = clone.querySelector(".gemini-copy-container");
        if (container) container.remove();
        const textControls = clone.querySelector(".gemini-text-controls");
        if (textControls) textControls.remove();
        const textToCopy = (clone.innerText || clone.textContent).trim();
        
        navigator.clipboard.writeText(textToCopy).then(() => {
          btn.innerHTML = "✅ Copied!";
          btn.style.background = "rgba(0, 150, 136, 0.2)";
          setTimeout(() => {
            btn.innerHTML = "📋 Copy";
            btn.style.background = "rgba(128, 128, 128, 0.2)";
          }, 2000);
        }).catch(err => {
          console.error("Failed to copy text: ", err);
          btn.innerHTML = "❌ Failed";
        });
      });
      
      btn.addEventListener("mouseenter", () => btn.style.background = "rgba(128, 128, 128, 0.3)");
      btn.addEventListener("mouseleave", () => {
        if(btn.innerHTML === "📋 Copy") btn.style.background = "rgba(128, 128, 128, 0.2)";
      });
      
      btnContainer.appendChild(btn);
      block.appendChild(btnContainer);
    });
  }

  // Set up an observer specifically for new messages
  const messageObserver = new MutationObserver(() => {
    addCopyButtons();
  });

  // Call it periodically to ensure it catches everything
  setInterval(addCopyButtons, 1500);
"""

content = content.replace("  console.log('YouTube Gemini Resizer: Extension loaded');\n})();", correct_code + "\n  console.log('YouTube Gemini Resizer: Extension loaded');\n})();")

with open('content.js', 'w') as f:
    f.write(content)
