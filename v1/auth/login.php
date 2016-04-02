<?php
	require '../config.php';
	$user_username = $_POST[$USERNAME_KEY];
	$user_password = $_POST[$PASSWORD_KEY];
	
	$sql = "SELECT * FROM users WHERE username = '$user_username' AND password = '$user_password' LIMIT 1";

	$result = $conn->query($sql);

	$rows = array();
	$response = array("success" => null, "payload" => $rows);
	if($result->num_rows == 1){
		$response["success"] = true;
		while($row = $result->fetch_assoc()) {
    		$rows[] = $row;
		}
		$response["payload"] = $rows;
	}else{
		$response["success"] = false;
	}
	echo json_encode($response);
?>