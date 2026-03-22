function toggleChatbot() {
    const window = document.getElementById('chatbot-window');
    window.style.display = window.style.display === 'none' ? 'flex' : 'none';
}

async function sendMessage() {
    const input = document.getElementById('chat-input');
    const messagesContainer = document.getElementById('chat-messages');
    const text = input.value.trim();
    
    if (!text) return;

    // Add user message
    const userDiv = document.createElement('div');
    userDiv.className = 'message user';
    userDiv.style.textAlign = 'right';
    userDiv.style.margin = '10px 0';
    userDiv.style.padding = '10px';
    userDiv.style.background = 'rgba(255,255,255,0.1)';
    userDiv.style.borderRadius = '10px';
    userDiv.innerText = text;
    messagesContainer.appendChild(userDiv);
    
    input.value = '';
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    try {
        const response = await fetch('/chatbot/api/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ message: text })
        });
        const data = await response.json();
        
        // Add bot message
        const botDiv = document.createElement('div');
        botDiv.className = 'message bot';
        botDiv.style.margin = '10px 0';
        botDiv.style.padding = '10px';
        botDiv.style.background = 'var(--primary-color)';
        botDiv.style.borderRadius = '10px';
        botDiv.style.lineHeight = '1.4';
        botDiv.innerHTML = data.response.replace(/\n/g, '<br>');
        messagesContainer.appendChild(botDiv);
        
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    } catch (e) {
        console.error('Chat error:', e);
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Splash Screen Logic
document.addEventListener('DOMContentLoaded', () => {
    // If not authenticated (checked via presence of login link or similar), show splash
    // For this demonstration, we'll assume the back-end handles the redirect to /login
    // But we can add a visual splash overlay if specified.
    console.log('EventElite Loaded');
});
