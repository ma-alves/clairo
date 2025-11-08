const onlineUser = JSON.parse(document.getElementById('current-id').textContent);
const onlineSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/online-status/'
)

onlineSocket.onopen = function (e) {
    console.log("Conexão de status online estabelecida.")
    onlineSocket.send(JSON.stringify({
        'type': 'open',
        'user_id': onlineUser,
    }))
}

window.addEventListener('beforeunload', function (e) {
    onlineSocket.send(JSON.stringify({
        'type': 'closed',
        'user_id': onlineUser,
    }))
})

onlineSocket.onclose = function (e) {
    console.log("Conexão de status online encerrada.")
}

onlineSocket.onerror = function (e) {
    console.error('Erro no WebSocket:', e);
};

onlineSocket.onmessage = function (e) {
    const data = JSON.parse(e.data)
    const statusType = data['status']
    const userId = data['user_id']

    const userStatusId = document.getElementById(`ws-${userId}`);

    if (statusType == true) {
        userStatusId.className = "inline-block w-3 h-3 bg-emerald-400 rounded-full ml-auto"
    } else {
        userStatusId.className = "hidden"
    }
}