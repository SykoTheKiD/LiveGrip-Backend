<?php
	require '../config.php';
	$user_username = $_POST[$USERNAME_KEY];
	$user_password = $_POST[$PASSWORD_KEY];
	$user_image = $_POST["profile_image"];

	if($user_username != null && $user_password != null){

		$sql = "INSERT INTO users (username, password, profile_image) VALUES ('$user_username', '$user_password', '$user_image')";

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