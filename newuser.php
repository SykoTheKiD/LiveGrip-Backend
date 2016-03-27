<?php
	require 'config.php';
	$user_username = $_POST[$USERNAME_KEY];
	$user_password = $_POST[$PASSWORD_KEY];
	$user_gcmID = $_POST[$GCM_ID_KEY];

	$sql = "INSERT INTO users (username, password, gcm_id) VALUES ('$user_username', '$user_password', '$user_gcmID')";

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