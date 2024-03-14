<?php
header("Access-Control-Allow-Origin: *");
header("Content-type: application/json; charset=utf-8");
include 'db.php' ;
// กำหนดค่าตัวแปร
$userID = $_POST['userID'];
$pressure = $_POST['pressure'];

try {
    

    // กำหนด query
    $sql = "INSERT INTO `measurement`(`userID`, `bloodpressure`) VALUES (?,?)";
    $stmt = $dbh->prepare($sql);

    // Bind parameters
    $stmt->bindParam(1, $userID);
    $stmt->bindParam(2, $pressure);

    // Execute the query
    $stmt->execute();

    // ปิดการเชื่อมต่อ
    $dbh = null;
} catch (PDOException $e) {
    // ตรวจจับและแสดงข้อผิดพลาด
    print "Error!:" . $e->getMessage() . "<br/>";
    die();
}
?>