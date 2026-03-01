document.addEventListener('DOMContentLoaded', () => {
    const shortenBtn = document.getElementById('shorten-btn');
    const urlInput = document.getElementById('url-input');
    const resultArea = document.querySelector('.result-area');
    const shortUrlDisplay = document.querySelector('.short-url-text');
    const copyHint = document.querySelector('.copy-hint');

    shortenBtn.addEventListener('click', async () => {
        const originalUrl = urlInput.value.trim();
        if (!originalUrl) {
            alert('Please enter a valid URL');
            return;
        }

        // Add loading state
        shortenBtn.innerText = 'Creating...';
        shortenBtn.disabled = true;

        try {
            const response = await fetch('/shorten', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ original_url: originalUrl }),
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to shorten URL');
            }

            const data = await response.json();
            const shortUrl = `${window.location.origin}/${data.short_code}`;

            // Reveal result with animation
            shortUrlDisplay.textContent = shortUrl;
            resultArea.classList.add('visible');
            copyHint.textContent = 'Click to Copy';
            
            // Re-animate the entrance
            resultArea.style.animation = 'none';
            resultArea.offsetHeight; // trigger reflow
            resultArea.style.animation = null;

        } catch (err) {
            alert(err.message);
        } finally {
            shortenBtn.innerText = 'Shorten';
            shortenBtn.disabled = false;
        }
    });

    // Copy to clipboard functionality
    document.querySelector('.short-url-box').addEventListener('click', () => {
        const textToCopy = shortUrlDisplay.textContent;
        navigator.clipboard.writeText(textToCopy).then(() => {
            copyHint.textContent = 'Copied to Clipboard!';
            copyHint.style.color = 'var(--accent-cyan)';
            
            setTimeout(() => {
                copyHint.textContent = 'Click to Copy';
                copyHint.style.color = 'var(--text-muted)';
            }, 3000);
        });
    });

    // Handle Enter key for input
    urlInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            shortenBtn.click();
        }
    });

    // Parallax effect on mouse move
    document.addEventListener('mousemove', (e) => {
        const mouseX = e.clientX / window.innerWidth - 0.5;
        const mouseY = e.clientY / window.innerHeight - 0.5;
        const card = document.querySelector('.glass-card');
        
        card.style.transform = `translateY(-5px) perspective(1000px) rotateY(${mouseX * 2}deg) rotateX(${-mouseY * 2}deg)`;
    });
});
