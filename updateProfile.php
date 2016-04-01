<?php
	require 'config.php';
	$user_username = $_POST[$USERNAME_KEY];
	$user_image = $_POST["profile_image"];

	if($user_username != null && $user_image != null){

		$sql = "UPDATE users SET profile_image='$user_image' WHERE username='$user_username'";

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