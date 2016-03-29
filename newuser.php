<?php
	require 'config.php';
	$user_username = $_POST[$USERNAME_KEY];
	$user_password = $_POST[$PASSWORD_KEY];

	if($user_username != null && $user_password != null){
		$sql = "INSERT INTO users (username, password) VALUES ('$user_username', '$user_password')";

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
	}else{
		echo json_encode(array('ERROR' => "NULL VALUES"));
	}
?>