var socket = io();

// No sé si estos sockets es necesario ponerlo o no, los he puesto por si acaso
socket.on('connect', function() {
    socket.emit('on_client', {data: 'connected'});
});

socket.on('disconnect', function() {
    socket.emit('on_client', {data: 'disconnected'});
});

function read_response() {
	var mydata = JSON.parse(text);
	alert(mydata[0].text);
	
	setTimeout(update, 500);
}