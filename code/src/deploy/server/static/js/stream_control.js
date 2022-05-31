
// ready event
$( document ).ready(function() {

$('#detectors').on('change', function (e) {
    var optionSelected = $("option:selected", this);
    var valueSelected = this.value;
    
    console.log(valueSelected);
    // make request to server

    $.ajax({
        url: '/change_detector?detector_type=' + valueSelected,
        type: 'GET',
        success: function (data) {
            console.log(data);
            alert('Detector changed to ' + valueSelected);
        }
    });

});

});

// function stop(){
//     $.ajax({
//         url: '/stop_detector',
//         type: 'GET',
//         success: function (data) {
//             console.log(data);
//             alert('Stream stopped');
//         }
//     });
// }

// function start(){
//     $.ajax({
//         url: '/start_detector',
//         type: 'GET',
//         success: function (data) {
//             console.log(data);
//             alert('Stream started');
//         }
//     });
// }