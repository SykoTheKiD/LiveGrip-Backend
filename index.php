<?php
	require('config.php');
	$sql = "SELECT * FROM events";

	$result = $conn->query($sql);

	$rows = array();
	$response = array("status" => null, "payload" => $rows);
	if($result->num_rows == 1){
		$response["status"] = true;
		while($row = $result->fetch_assoc()) {
    		$rows[] = $row;
		}
		$response["payload"] = $rows;
	}else{
		$response["status"] = false;
	}
	echo json_encode($response);
?>