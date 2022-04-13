var socket = io();

socket.on('connect', function() {
    socket.emit('on_client', {data: 'New client connected'});
});

socket.on('disconnect', function() {
    socket.emit('on_client', {data: 'Client disconnected'});
});

function update(){
    console.log("Reading Sensors")    
    
    socket.emit('get_sensors', "get");

    setTimeout(update, 1000); //agafem valors cada sensor a cada segon
}


// We receive the data from sensors
socket.on('receive_sensors',  function (data) {
    console.log(data);
    // parse json data
    var sensors = JSON.parse(data);
    // update sensors
    
    Object.keys(sensors).forEach(function(key) {
        var sensor_value = sensors[key];
        $('#' + key).html(sensor_value);
    });
});


$( document ).ready(function() {
    console.log( "ready!" );
    update();
});
