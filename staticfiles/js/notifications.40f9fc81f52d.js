document.addEventListener("DOMContentLoaded", function () {
    function connectWebSocket() {
        const notificationSocket = new WebSocket(
            'ws://' + window.location.host + '/ws/notifications/'
        );

        notificationSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            alert('Notification: ' + data.message);
        };

        notificationSocket.onclose = function(e) {
            console.error('WebSocket closed unexpectedly');
        };
    }

    connectWebSocket();
});
