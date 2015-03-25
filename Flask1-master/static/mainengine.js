$(document).ready(function(){

	//assign callback whenever user change value of num1 and num2
	$("#inputNum1").change(updateSum);
	$("#inputNum2").change(updateSum);
});

function updateSum(){
	var request = $.ajax({
		url: "/calculateSum",
		method: "GET",
		data: { num1 : $("#inputNum1").val(), num2 : $("#inputNum2").val() }
		//dataType: "json"
	});
	request.done(function( msg ) {
		console.log(msg);
		var ResultStruct = JSON.parse(msg);
		$("#pResult").html(ResultStruct.result);
	});
	request.fail(function( jqXHR, textStatus ) {
		alert( "Request failed: " + textStatus );
	});


}



