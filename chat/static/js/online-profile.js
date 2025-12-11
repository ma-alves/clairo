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
    const profileStatusId = document.getElementById("ws-profile");
    
    if (profileStatusId) {
        const profileOwnerId = Number(profileStatusId.dataset.profileId);
        if (profileOwnerId === Number(userId)) {
            if (statusType === true || statusType === 'true') {
                profileStatusId.className = "absolute bottom-2 right-2 bg-emerald-400 w-6 h-6 rounded-full border-2 border-white";
            } else {
                profileStatusId.className = "hidden";
            }
        }
    }
}