<?php
	$host_name  = "vagrant-ubuntu-trusty-64";
	$database   = "wrestlechat";
	$user_name  = "root";
	$password   = "pass";
	$connection = mysqli_connect($host_name, $user_name, $password, $database);
	if (mysqli_connect_errno()){
	    echo "Failed to connect to MySQL: " . mysqli_connect_error();
	}
	header('Content-Type: application/json');
	$event_id = $_POST["event_id"];
	$user_id = $_POST["user_id"];
	$body = $_POST["body"];

	$sql = "INSERT INTO messages (event_id, user_id, body)
	VALUES ('$event_id', '$user_id', '$body')";

	$success = null;
	$error = null;
	if ($connection->query($sql) === TRUE) {
    	$success = true;
	} else {
		$success = false;
    	$error = $connection->error;
	}

	$rows = array("success" => $success, "payload" => $error);
	echo json_encode($rows);
?>