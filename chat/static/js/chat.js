const roomName = JSON.parse(document.getElementById('chat_uuid').textContent);
const currentUser = JSON.parse(document.getElementById('current-id').textContent);

const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
);

chatSocket.onmessage = function (e) {
    try {
        const data = JSON.parse(e.data);
        if (data.error) {
            console.error('Erro no servidor:', data.error);
            alert(data.error);
            return;
        } else if (data.message) {
            const chatMessages = document.querySelector('#chat_messages');
            const messageElement = document.createElement('li');

            if (data.user === currentUser) {
                messageElement.innerHTML = `
                        <div class="flex justify-end">
                            <div class="bg-black text-white rounded-l-lg rounded-lg p-2 max-w-[75%]">
                                <span>${data.message}</span>
                            </div>
                        </div>
                        <span class="flex justify-end text-xs text-gray-500 mt-1">${data.time}</span>`;
            } else {
                messageElement.innerHTML = `
                        <div class="flex justify-start">
                            <div class="bg-emerald-300 p-2 max-w-[75%] rounded-lg">
                                <span>${data.message}</span>
                            </div>
                        </div>
                        <span class="text-xs text-gray-500 mt-1">${data.time}</span>`;
            }
            chatMessages.appendChild(messageElement);

            // Scroll automático
            const chatContainer = document.querySelector('#chat_container');
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    } catch (error) {
        console.error('Erro ao processar mensagem:', error);
    }
};

chatSocket.onclose = function (e) {
    console.log('Chat socket desconectado.');
};

chatSocket.onerror = function (e) {
    console.error('Erro no WebSocket:', e);
};

document.querySelector('#chat-message-input').focus();

document.querySelector('#chat-message-input').onkeyup = function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function (e) {
    const messageInput = document.querySelector('#chat-message-input');
    const chat_message = messageInput.value.trim();

    if (chat_message) {
        chatSocket.send(JSON.stringify({
            'message': chat_message,
        }));
        messageInput.value = '';
    }
};

function scrollToBottom(time = 0) {
    setTimeout(function () {
        const container = document.getElementById('chat_container');
        container.scrollTop = container.scrollHeight;
    }, time);
}
scrollToBottom()