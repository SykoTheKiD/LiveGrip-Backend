<?php
	require '../config.php';
	$event_id = $_POST["event_id"];
	$user_id = $_POST["user_id"];
	$body = $_POST["body"];

	$sql = "INSERT INTO messages (event_id, user_id, body) VALUES ('$event_id', '$user_id', '$body')";

	$success = null;
	$error = null;
	if ($conn->query($sql) === TRUE) {
    	$success = true;
	} else {
		$success = false;
    	$error = $conn->error;
	}

	$rows = array("success" => $success, "payload" => $error);
	echo json_encode($rows);
?>