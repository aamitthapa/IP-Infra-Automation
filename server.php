<?php
set_time_limit(0);

// arquivo cujo conteúdo será enviado ao cliente
$dataFileName = 'Test_Result/test_log';

while ( true )
{
	$requestedTimestamp = isset ( $_GET [ 'timestamp' ] ) ? (int)$_GET [ 'timestamp' ] : null;

	// o PHP faz cache de operações "stat" do filesystem. Por isso, devemos limpar esse cache
	clearstatcache();
	$modifiedAt = filemtime( $dataFileName );

	if ( $requestedTimestamp == null || $modifiedAt > $requestedTimestamp )
	{
		$handle = fopen("Test_Result/test_log", "rb");
		$data = stream_get_contents($handle);
		fclose($handle);
#		$test= fopen("test_auto.txt", "w");
#		fwrite($test, $data);
#		fclose($test);
	#	$data = file_get_contents( $dataFileName );

		$arrData = array(
			'content' => $data,
			'timestamp' => $modifiedAt
		);
#		$file = fopen("autoupdate.txt","w");
#		fwrite($file, $data);
		$json = json_encode( $arrData );
		echo $json;
    if(strpos($data, "Test Set Complete!!!!!!") !== false)
    {
    $file= fopen("test_set_select.php", "w");
    $check = stream_get_contents($file);
    $str = str_replace('<input type="submit" name="stop" value="Stop"/>','<input type="submit" name="Test Set Complete!!!!" value="Test Set Complete!!!!"/>', $check);
    fwrite($file, $str);
    header("Location: test_set_select.php");
    }

		break;
	}
	else
	{
		sleep( 1 );
		continue;
	}
}
