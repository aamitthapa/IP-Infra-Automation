function getContent( timestamp )
{
	var queryString = { 'timestamp' : timestamp };
	var check='Test Set Complete!!!!!!';
	var check1='utsav';
	$.get ( 'server.php' , queryString , function ( data )
	{
		var obj = jQuery.parseJSON( data );
		var myJSON = JSON.stringify(obj);
		var check2 = myJSON.indexOf("Test Set Complete!!!!!!");
//		window.alert(check2);
		document.getElementById("response").innerHTML = obj.content.toString();
		if (check2 !== -1) {
		//	document.getElementById("complete").innerHTML = "Test Set Completed";
			window.location = "test_set_pre_complete.php"; }
		getContent( obj.timestamp );
	});
}

$( document ).ready ( function ()
{
	getContent();
});
