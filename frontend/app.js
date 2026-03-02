document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chat-messages');

    // Enable/disable send button based on input
    messageInput.addEventListener('input', () => {
        sendButton.disabled = messageInput.value.trim() === '';
    });

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const message = messageInput.value.trim();
        if (!message) return;

        // 1. Add user message to UI
        addMessage(message, 'user');

        // Clear input and disable button
        messageInput.value = '';
        sendButton.disabled = true;

        // 2. Show typing indicator
        const typingId = showTypingIndicator();

        try {
            // 3. Send to backend
            const response = await fetch('https://azeembot-ai.onrender.com/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();

            // 4. Remove typing indicator
            removeTypingIndicator(typingId);

            if (response.ok) {
                // 5. Add bot message
                addMessage(data.reply, 'bot');
            } else {
                // Handle API error
                addMessage(data.detail || 'Sorry, I encountered an error. Please try again.', 'bot', true);
            }

        } catch (error) {
            console.error('Error:', error);
            removeTypingIndicator(typingId);
            addMessage('Network error. Please check your connection and try again.', 'bot', true);
        }
    });

    function addMessage(text, sender, isError = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message ${isError ? 'error-message' : ''}`;

        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        messageDiv.innerHTML = `
            <div class="message-content">${escapeHTML(text)}</div>
            <span class="timestamp">${time}</span>
        `;

        chatMessages.appendChild(messageDiv);
        scrollToBottom();
    }

    function showTypingIndicator() {
        const id = 'typing-' + Date.now();
        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing-indicator';
        typingDiv.id = id;

        typingDiv.innerHTML = `
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
        `;

        chatMessages.appendChild(typingDiv);
        scrollToBottom();
        return id;
    }

    function removeTypingIndicator(id) {
        const element = document.getElementById(id);
        if (element) {
            element.remove();
        }
    }

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Basic HTML escaping to prevent XSS
    function escapeHTML(str) {
        return str.replace(/[&<>'"]/g,
            tag => ({
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                "'": '&#39;',
                '"': '&quot;'
            }[tag])
        );
    }
});
