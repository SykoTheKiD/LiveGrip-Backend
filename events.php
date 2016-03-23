<?php
	$host_name  = "vagrant-ubuntu-trusty-64";
	$database   = "wrestlechat";
	$user_name  = "root";
	$password   = "pass";
	$conn = mysqli_connect($host_name, $user_name, $password, $database);
	$rows = array();
	$response = array("success" => null, "payload" => $rows);
	if (mysqli_connect_errno()){
		$response["success"] = false;
	    // echo "Failed to connect to MySQL: " . mysqli_connect_error();
	}
	header('Content-Type: application/json');
	$sql = "SELECT * FROM events";

	$result = $conn->query($sql);

	
	while($row = $result->fetch_assoc()) {
    		$rows[] = $row;
	}
	$response["success"] = true;
	$response["payload"] = $rows;
	// if($result->num_rows == 1){
		
	// 	while($row = $result->fetch_assoc()) {
 //    		$rows[] = $row;
	// 	}
	// }else{
	// 	$response["success"] = false;
	// 	var_dump($rows);
	// }
	echo json_encode($response);

?>