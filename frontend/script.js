const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const chatForm = document.getElementById('chatForm');

// Add message to chat
function addMessage(text, sender) {
  const msg = document.createElement('div');
  msg.classList.add('message', sender);
  msg.textContent = text;
  chatMessages.appendChild(msg);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Fetch bot reply from backend
async function fetchBotReply(promptText) {
  try {
    const url = `http://13.51.86.244:8000/prompt?prompt=${encodeURIComponent(promptText)}`;
    const response = await fetch(url, {
        
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      
    });
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const data = await response.json();
    return data.response || "Sorry, no response from server.";
  } catch (error) {
    return "Error fetching response: " + error.message;
  }
}

// Handle submit
chatForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const userText = chatInput.value.trim();
  if (!userText) return;

  addMessage(userText, 'user');
  chatInput.value = '';
  chatInput.focus();

  addMessage("Athena is typing...", 'bot');

  const botReplyText = await fetchBotReply(userText);

  // Remove "Athena is typing..." placeholder before adding actual reply
  const typingMsg = chatMessages.querySelector('.message.bot:last-child');
  if (typingMsg) {
    chatMessages.removeChild(typingMsg);
  }

  addMessage("Athena: " + botReplyText, 'bot');
});
