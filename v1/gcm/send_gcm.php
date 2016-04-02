<?php

    require '../config.php';
    require 'Push.php';

    $sql = "SELECT gcm_id FROM users";

    $result = $conn->query($sql);

    $rows = array();
    while($row = $result->fetch_assoc()) {
        if($row["gcm_id"] != null){
            $rows[] = $row;
        }
    }
    
    $push = new Push();

    $push->setTitle("Wrestlemania 32 is LIVE!");
    $push->setMessage("The chat for WM 32 is now open!");
    $push->setTickerText("LiveGrip v2.0");
    $push->setUrl("http://www.gospelherald.com/data/images/full/16855/wrestlemania-32.jpg");
	$message = $push->getPush();

    $rows = (array_filter($rows));

    var_dump($rows);

	$fields = array(
        'registration_ids' => $rows,
        'data' => $message
    );

    $url = 'https://gcm-http.googleapis.com/gcm/send';
 
    $headers = array(
        'Authorization:key=AIzaSyDpWCGYdDIHCrjFuPljfjts_BjoXvnXcsA',
        'Content-Type:application/json'
    );

 //    // Open connection
    $ch = curl_init();

    // // Set the url, number of POST vars, POST data
    curl_setopt($ch, CURLOPT_URL, $url);

    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    // // Disabling SSL Certificate support temporarly
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);

    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($fields));

    // // Execute post
    $result = curl_exec($ch);
    if ($result === FALSE) {
        die('Curl failed: ' . curl_error($ch));
    }

    // // Close connection
    curl_close($ch);

    echo $result;
?>