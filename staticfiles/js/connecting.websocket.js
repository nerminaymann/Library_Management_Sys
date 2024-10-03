const bookAvailabilitySocket = new WebSocket(
    'ws://' + window.location.host + '/ws/book-availability/'
);

bookAvailabilitySocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    alert(data.message);  // Notify the user when book availability changes
};

bookAvailabilitySocket.onclose = function(e) {
    console.error('Book availability socket closed unexpectedly');
};
