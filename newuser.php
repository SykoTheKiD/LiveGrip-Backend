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
	$user_username = $_POST["username"];
	$user_password = $_POST["password"];
	$user_email = $_POST["email"];

	$sql = "INSERT INTO users (username, email, password)
	VALUES ('$user_username', '$user_email', '$user_password')";

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