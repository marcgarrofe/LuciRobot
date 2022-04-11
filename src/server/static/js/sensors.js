var socket = io();

socket.on('connect', function() {
    socket.emit('on_client', {data: 'New client connected'});
});

socket.on('disconnect', function() {
    socket.emit('on_client', {data: 'Client disconnected'});
});

socket.on('get_sensors', function (data) {
    console.log(data);
    // parse json data
    var sensors = JSON.parse(data.data);
    // update sensors
    
    Object.keys(sensors).forEach(function(key) {
        var sensor_value = jsonData[key];
        $('#' + key).html(sensor_value);
    });
});


