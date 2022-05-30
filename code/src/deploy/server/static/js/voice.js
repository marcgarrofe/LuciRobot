function write_sentence(sentence){
	// <div class="transcript-sentence">
    //                                     <div>
    //                                         <h6 class=" mb-2 text-muted" id="timestamp">00:00:00 - </h6>
    //                                     </div>
    //                                     <div>
    //                                         <h6 class="" id="text">I am drowning</h6></h6>
    //                                     </div>
    //                         </div>

	var div = document.createElement("div");
	div.className = "transcript-sentence";
	
	var div_1 = document.createElement("div");
	var div_2 = document.createElement("div");
	
	var h6_1 = document.createElement("h6");
	h6_1.className = " mb-2 text-muted";
	h6_1.id = "timestamp";

	var h6_2 = document.createElement("h6");
	h6_2.className = "";
	h6_2.id = "text";
	
	// set timestamp
	var date = new Date();
	var time = date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();
	h6_1.innerHTML = time + " - ";


	var text_2 = document.createTextNode(sentence);
	
	h6_2.appendChild(text_2);
	
	div_1.appendChild(h6_1);
	div_2.appendChild(h6_2);
	
	div.appendChild(div_1);
	div.appendChild(div_2);

	document.getElementById("transcript-column").appendChild(div);
}

function read_response() {
	
	// read voice_response.json file at static folder

	$.getJSON("/static/voice_response.json", function(data) {
		// parse voice_response.json file
		print(data);
		
		try {
			var voice_response_json = JSON.parse(data);


			write_sentence(voice_response_json.text);
			
			setTimeout(read_response, 500);
		}
		catch(err) {
			
			console.log(err);
		}

		
	});
}

$( document ).ready(function() {
    console.log( "Ready voice !" );
	read_response();
});