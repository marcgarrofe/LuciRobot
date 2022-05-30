var socket = io();

var sensors_dict = {"gas_concentration":Array.apply(0, Array(60)), "ultrasound_sensor_1_distance":Array.apply(0, Array(60)),"ultrasound_sensor_2_distance":Array.apply(0, Array(60)),"dht11_humidity":Array.apply(0, Array(60)),"dht11_temp":Array.apply(0, Array(60)) }
var xAxis = Array.from({length: 60}, (_, i) => i + 1);
//var sensor1 = [60,20,30,55,30,1000,40]	// Solo usado para hardcodear resultados

socket.on('connect', function() {
    socket.emit('on_client', {data: 'connected'});
});

socket.on('disconnect', function() {
    socket.emit('on_client', {data: 'disconnected'});
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
		
		// if size of array >60 we delete the first element
		if(sensors_dict[key].push(sensor_value) >= 60){
			sensors_dict[key].shift();
		}
		
    });
});


$( document ).ready(function() {
    console.log( "ready!" );
    // update();

    var exampleModal = document.getElementById('exampleModal')
    
    exampleModal.addEventListener('show.bs.modal', function (event) {
      // Button that triggered the modal
      var button = event.relatedTarget
      // Extract info from data-bs-* attributes
      var sensorName = button.getAttribute('data-bs-sensor-name')
      var sensorId = button.getAttribute('data-bs-sensor-id')
      // If necessary, you could initiate an AJAX request here
      // and then do the updating in a callback.
      //
      // Update the modal's content.
      var modalTitle = exampleModal.querySelector('.modal-title')
      var modalBodyInput = exampleModal.querySelector('.modal-body input')

      modalTitle.textContent = 'Sensor ' + sensorName + ' graph'
      modalBodyInput.value = sensorName

      const ctx = document.getElementById('myChart').getContext('2d');
    
      const myChart = new Chart(document.getElementById("myChart"), {
        type: 'line',
        data: {
          labels: xAxis,
          datasets: [{ 
          // Mostrará la data de los últimos 60 segundos del sensor
              data: sensors_dict[sensorName], //También puede ser que sea modalBodyInput pero tampoco lo sé
              label: sensorId, // También puede ser que sea modalTitle pero no lo sé
              borderColor: "#3e95cd",
              fill: false
            },
          ]
        },
        options: {
          title: {
            display: true,
            text: 'Sensor ' + sensorName + ' graph (last 3 minutes)'
          }
        }
      });
    })

    
});


