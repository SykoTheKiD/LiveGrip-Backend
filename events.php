<?php
	require 'config.php';
	$rows = array();
	$response = array("success" => null, "payload" => $rows);
	$sql = "SELECT * FROM events";

	$result = $conn->query($sql);
	
	while($row = $result->fetch_assoc()) {
    	$rows[] = $row;
	}
	$response["success"] = true;
	$response["payload"] = $rows;

	echo json_encode($response);

?>