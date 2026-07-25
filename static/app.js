// UrutauLLM-Lab - Frontend JS

let currentChallengeId = '00';
let isWaiting = false;

document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    setupChallengeCards();
    setupAuth();
    refreshAuth();
});

function setupAuth() {
    document.getElementById('login-btn').addEventListener('click', doLogin);
    document.getElementById('logout-btn').addEventListener('click', doLogout);
    document.getElementById('login-username').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') doLogin();
    });
}

async function refreshAuth() {
    try {
        const res = await fetch('/api/me');
        const me = await res.json();
        renderAuth(me.username);
    } catch (_) { /* offline is fine */ }
}

function renderAuth(username) {
    const out = document.getElementById('auth-logged-out');
    const inn = document.getElementById('auth-logged-in');
    if (username) {
        document.getElementById('auth-username').textContent = username;
        out.hidden = true;
        inn.hidden = false;
    } else {
        out.hidden = false;
        inn.hidden = true;
    }
}

async function doLogin() {
    const username = document.getElementById('login-username').value.trim();
    if (!username) return;
    const res = await fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username }),
    });
    if (res.ok) {
        const data = await res.json();
        renderAuth(data.username);
    }
}

async function doLogout() {
    await fetch('/logout', { method: 'POST' });
    renderAuth(null);
}

function setupEventListeners() {
    const sendBtn = document.getElementById('send-btn');
    const userInput = document.getElementById('user-input');

    sendBtn.addEventListener('click', sendMessage);

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !isWaiting) {
            sendMessage();
        }
    });

    document.getElementById('hint-btn').addEventListener('click', showHint);
    document.getElementById('writeup-btn').addEventListener('click', showWriteup);
}

function setupChallengeCards() {
    const cards = document.querySelectorAll('.challenge-card');
    cards.forEach(card => {
        card.addEventListener('click', () => {
            // Marca como ativo
            cards.forEach(c => c.classList.remove('active'));
            card.classList.add('active');

            // Atualiza challenge atual
            currentChallengeId = card.dataset.challengeId;
            const name = card.querySelector('h3').textContent.trim();
            document.getElementById('current-challenge-name').textContent = name;

            // Limpa chat
            clearChat();
            addSystemMessage(`Challenge selecionado: ${name}. Boa sorte! 🦉`);
        });
    });
}

async function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();

    if (!message || isWaiting) return;

    isWaiting = true;
    document.getElementById('send-btn').disabled = true;

    addMessage('user', message);
    input.value = '';

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                challenge_id: currentChallengeId
            })
        });

        if (!response.ok) {
            throw new Error('Erro na requisição');
        }

        const data = await response.json();
        addMessage('bot', data.response);

        // Verifica se achou a flag
        if (data.flag_found) {
            showFlagBanner();
        }

    } catch (error) {
        addMessage('system', `❌ Erro: ${error.message}`);
    } finally {
        isWaiting = false;
        document.getElementById('send-btn').disabled = false;
        input.focus();
    }
}

function addMessage(type, text) {
    const messagesDiv = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;

    const p = document.createElement('p');
    p.textContent = text;
    messageDiv.appendChild(p);

    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function addSystemMessage(text) {
    addMessage('system', text);
}

function clearChat() {
    const messagesDiv = document.getElementById('chat-messages');
    messagesDiv.innerHTML = '';
    hideFlagBanner();
}

function showFlagBanner() {
    document.getElementById('flag-banner').classList.remove('hidden');
    setTimeout(() => {
        document.getElementById('flag-banner').classList.add('hidden');
    }, 5000);
}

function hideFlagBanner() {
    document.getElementById('flag-banner').classList.add('hidden');
}

async function showHint() {
    try {
        const response = await fetch(`/api/challenges/${currentChallengeId}/hint`);
        const data = await response.json();
        addSystemMessage(`💡 Dica: ${data.hint}`);
    } catch (error) {
        addSystemMessage('❌ Erro ao buscar dica');
    }
}

async function showWriteup() {
    try {
        const response = await fetch(`/api/challenges/${currentChallengeId}/writeup`);
        const data = await response.json();
        addSystemMessage(`📖 Write-up: ${data.writeup}`);
    } catch (error) {
        addSystemMessage('❌ Erro ao buscar write-up');
    }
}
