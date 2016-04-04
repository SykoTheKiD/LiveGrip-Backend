<?php
	require '../config.php';
	$user_username = $_POST[$USERNAME_KEY];
	$user_gcmID = $_POST["gcm_id"];

	ini_set('post_max_size','5M');

	if(isset($user_username) && isset($user_gcmID)){
		$sql = "UPDATE users SET gcm_id='$user_gcmID' WHERE username='$user_username'";

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
		var_dump($user_username);
		var_dump($user_gcmID);
		var_dump($_POST);
		echo json_encode(array('ERROR' => "NULL VALUES"));
	}
?>