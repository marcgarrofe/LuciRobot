// var socket = io();

// socket.on('connect', function() {
//     socket.emit('on_client', {data: 'connected'});
// });

// socket.on('disconnect', function() {
//     socket.emit('on_client', {data: 'disconnected'});
// });

// // We receive the data from sensors
// socket.on('receive_sensors',  function (data) {
//     console.log(data);
//     parse_sensors  (data);
// });

// // We receive the data from sensors
// socket.on('message',  function (data) {
//     console.log(data);
//     parse_sensors  (data);
// });




function update(){
    console.log("Reading Sensors");    
    
    // socket.emit('get_sensors', "get");
    // read sensors.json file and update the values

    $.getJSON("/static/sensors.json", function(data) {
        console.log("GOT JSON");
        console.log(data);
        parse_sensors(data);
    });

    setTimeout(update, 1000); //agafem valors cada sensor a cada segon
}


function parse_sensors(data){
    console.log("Parsing Sensors")
    // get if data is empty or not
    if(data.length == 0){
        console.log("Empty data")
        return;
    }
    // parse json data
    var sensors = JSON.parse(data);
    // update sensors
    
    Object.keys(sensors).forEach(function(key) {
        var sensor_value = sensors[key];
        $('#' + key).html(sensor_value);
    });
}




$( document ).ready(function() {
    console.log( "ready!" );
    
    update();
    
    var exampleModal = document.getElementById('exampleModal')
    exampleModal.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    var button = event.relatedTarget
    // Extract info from data-bs-* attributes
    var recipient = button.getAttribute('data-bs-sensor-name')
    // If necessary, you could initiate an AJAX request here
    // and then do the updating in a callback.
    //
    // Update the modal's content.
    var modalTitle = exampleModal.querySelector('.modal-title')
    var modalBodyInput = exampleModal.querySelector('.modal-body input')

    modalTitle.textContent = 'Sensor ' + recipient + ' graph'
    modalBodyInput.value = recipient
    })

    const ctx = document.getElementById('myChart').getContext('2d');
    
    const myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
            datasets: [{
                label: '# of Votes',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});


