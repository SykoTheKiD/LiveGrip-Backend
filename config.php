<?php
$host_name  = "localhost";
$database   = "livegrip";
$user_name  = "root";
$password   = "1Drizzydrake";
$conn = mysqli_connect($host_name, $user_name, $password, $database);
if (mysqli_connect_errno()){
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
}
header('Content-Type: application/json');

$USERNAME_KEY = "username";
$PASSWORD_KEY = "password";

?>
