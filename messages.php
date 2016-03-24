<?php
	require 'config.php';
	$event_id = $_POST["event_id"];

	$sql = "SELECT u.username, u.profile_image, m.body, e.name FROM users u, events e, messages m WHERE m.user_id = u.id AND m.event_id = '$event_id' AND e.id = '$event_id'";

	$result = $conn->query($sql);

	$rows = array();
	$response = array("success" => null, "payload" => $rows);
	$response["success"] = true;
	while($row = $result->fetch_assoc()) {
    	$rows[] = $row;
	}
	$response["payload"] = $rows;
	echo json_encode($response);
?>