$(document).ready(function(){
	$.getJSON('/letters', function(data){
		console.log(data);
	})
});