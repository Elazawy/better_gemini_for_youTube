// Add copy buttons to Gemini responses
  function addCopyButtons() {
    if (!geminiContainer) return;

    // Selectors for message blocks in YouTube Gemini (heuristic)
    const messageBlocks = geminiContainer.querySelectorAll(
      '[class*="message-body"], [class*="model-response"], [class*="response-content"], .message-content, [class*="gemini-message"], ytd-engagement-panel-section-list-renderer [role="listitem"] div:not([class*="user"])'
    );

    messageBlocks.forEach(block => {
      // Only target blocks that don't already have our button
      if (block.querySelector('.gemini-copy-btn')) return;

      // Skip if it looks like a user prompt or input field
      if (block.tagName === 'INPUT' || block.tagName === 'TEXTAREA' || block.hasAttribute('contenteditable')) return;

      // Skip if it's too small
      if (!block.textContent || block.textContent.trim().length < 5) return;

      // Skip if it contains an avatar (often user message)
      if (block.querySelector('img[class*="avatar"]')) return;

      const btnContainer = document.createElement('div');
      btnContainer.className = 'gemini-copy-container';
      btnContainer.style.marginTop = '8px';
      btnContainer.style.textAlign = 'left';

      const btn = document.createElement('button');
      btn.className = 'gemini-copy-btn';
      btn.innerHTML = '📋 Copy';
      btn.title = 'Copy response to clipboard';

      // Inline styles just in case css doesn't load fully for dynamically added elements
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

      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        
        const clone = block.cloneNode(true);
        const container = clone.querySelector('.gemini-copy-container');
        if (container) container.remove();
        
        // Remove text controls if somehow inside
        const textControls = clone.querySelector('.gemini-text-controls');
        if (textControls) textControls.remove();

        const textToCopy = (clone.innerText || clone.textContent).trim();

        navigator.clipboard.writeText(textToCopy).then(() => {
          btn.innerHTML = '✅ Copied!';
          btn.style.background = 'rgba(0, 150, 136, 0.2)';
          setTimeout(() => {
            btn.innerHTML = '📋 Copy';
            btn.style.background = 'rgba(128, 128, 128, 0.2)';
          }, 2000);
        }).catch(err => {
          console.error('Failed to copy text: ', err);
          btn.innerHTML = '❌ Failed';
        });
      });

      // Add hover effect
      btn.addEventListener('mouseenter', () => btn.style.background = 'rgba(128, 128, 128, 0.3)');
      btn.addEventListener('mouseleave', () => {
        if(btn.innerHTML === '📋 Copy') btn.style.background = 'rgba(128, 128, 128, 0.2)';
      });

      btnContainer.appendChild(btn);
      block.appendChild(btnContainer);
    });
  }
