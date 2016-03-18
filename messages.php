<?php
	$host_name  = "vagrant-ubuntu-trusty-64";
	$database   = "wrestlechat";
	$user_name  = "root";
	$password   = "pass";
	$conn = mysqli_connect($host_name, $user_name, $password, $database);
	if (mysqli_connect_errno()){
	    echo "Failed to connect to MySQL: " . mysqli_connect_error();
	}
	header('Content-Type: application/json');
	$event_id = $_POST["event_id"];

	$sql = "SELECT m.user_id, m.body, e.name FROM events e, messages m WHERE m.event_id = '$event_id' AND e.id = '$event_id'";

	$result = $conn->query($sql);

	$rows = array();
	$response = array("success" => null, "payload" => $rows);
	$response["success"] = true;
	while($row = $result->fetch_assoc()) {
    	$rows[] = $row;
	}
	$response["payload"] = $rows;
	echo json_encode($response);
?>