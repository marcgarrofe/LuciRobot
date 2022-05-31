var socket = io();

var sensors_dict = { 
  "gas_concentration": new Array(60).fill(0), 
  "ultrasound_sensor_1_distance": new Array(60).fill(0),
  "ultrasound_sensor_2_distance": new Array(60).fill(0),
  "dht11_humidity": new Array(60).fill(0), 
  "dht11_temp": new Array(60).fill(0),
}

var myChart = undefined;
var currentOpenSensor = undefined;

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

    try {
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

      // update chart
      if(myChart != undefined){
        
        if (currentOpenSensor != undefined && key == currentOpenSensor) {
          myChart.data.datasets[0].data = sensors_dict[key];
          myChart.data.datasets[0].label = key;
          myChart.update();
        }
  
  
      }


      });
    } catch (error) {
        console.log(error);
    }
    
});

socket.on('cpu_temp', function (data) {
    // console.log(data);
    $('#cpu_temp').html(data);

    badge = document.getElementById("cpu_temp_badge");
    // if data > 75 we change the color of the text
    if(data > 75){
      // replace bg-success with bg-danger
      badge.className = badge.className.replace(/\bbg-success\b/g, 'bg-danger');
    }
    else{
      // replace bg-danger with bg-success
      badge.className = badge.className.replace(/\bbg-danger\b/g, 'bg-success');
    }

});


socket.on('termal_camera_range', function(data){
    console.log(data);
    // term-graph
    const myChart = new Chart(document.getElementById("term-graph"), {
      type: 'line',
      data: {
        labels: xAxis,
        datasets: [{ 
        // Mostrará la data de los últimos 60 segundos del sensor
            data: data, //También puede ser que sea modalBodyInput pero tampoco lo sé
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
});


$( document ).ready(function() {
    console.log( "ready!" );
    update();

    var exampleModal = document.getElementById('exampleModal')

    const ctx = document.getElementById('myChart').getContext('2d');
    var sensorName = 'gas_concentration';
    var sensorId = 'gas_concentration';
    
    myChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: xAxis,
        datasets: [{ 
        // Mostrará la data de los últimos 60 segundos del sensor
            data: sensors_dict[sensorId], //También puede ser que sea modalBodyInput pero tampoco lo sé
            label: sensorName, // También puede ser que sea modalTitle pero no lo sé
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
      // var modalBodyInput = exampleModal.querySelector('.modal-body input')

      modalTitle.textContent = 'Sensor ' + sensorName + ' graph'
      // modalBodyInput.value = sensorName
      currentOpenSensor = sensorId;

      console.log(sensors_dict);
      console.log(sensors_dict[sensorId]);
      
      myChart.data.datasets[0].data = sensors_dict[sensorId];
      myChart.data.datasets[0].label = sensorName;


      myChart.update();

    } );
   
});


