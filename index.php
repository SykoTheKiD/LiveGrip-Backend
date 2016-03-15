<?php

require '../Slim/Slim.php';

\Slim\Slim::registerAutoloader();

$app = new \Slim\Slim();

$version = "v1"
$host_name  = "db591872347.db.1and1.com";
$database   = "db591872347";
$user_name  = "dbo591872347";
$password   = "1Drizzydrake!";
$connection = mysqli_connect($host_name, $user_name, $password, $database);
if (mysqli_connect_errno()){
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
}
$sql = "SELECT * FROM Posts ORDER BY id DESC";
$result = mysqli_query($connection, $sql) or die("Error in Selecting " . mysqli_error($connection));

// POST METHODS
$app->post($version .'/auth/login', function () use ($app) {
    $tempArray = [];
    while($row = mysqli_fetch_assoc($result)){
        $tempArray[] = $row;
    }
    $response = $app->response();
    $response['Content-Type'] = 'application/json';
    $response->status(200);
    $response->body(json_encode($tempArray));
});

$app->run();