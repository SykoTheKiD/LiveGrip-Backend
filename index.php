<?php
	$host_name  = "vagrant-ubuntu-trusty-64";
	$database   = "wrestlechat";
	$user_name  = "root";
	$password   = "pass";
	$conn = mysqli_connect($host_name, $user_name, $password, $database);
	if (mysqli_connect_errno()){
	    echo "Failed to connect to MySQL: " . mysqli_connect_error();
	}

	$sql = "SELECT * FROM events";

	$result = $conn->query($sql);

	$rows = array();
	$response = array("status" => null, "payload" => $rows);
	if($result->num_rows == 1){
		$response["status"] = true;
		while($row = $result->fetch_assoc()) {
    		$rows[] = $row;
		}
		$response["payload"] = $rows;
	}else{
		$response["status"] = false;
	}
	echo json_encode($response);

	// if ($result->num_rows > 0) {
 //    	// output data of each row
 //    	while($row = $result->fetch_assoc()) {
 //        	echo "id: " . $row["id"]. " - Name: " . $row["username"]. " " . $row["password"]. "<br>";
 //    	}
	// } else {
 //    	echo "0 results";
	// }

	// $rows = array("success" => $success, "reason" => $error);
	// while($r = mysqli_fetch_assoc($sql)) {
    	// $rows[] = $r;
	// }
	// echo json_encode($rows);
?>