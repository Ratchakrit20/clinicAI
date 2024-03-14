<?php
header("Access-Control-Allow-Origin: *");
header("Content-type: application/json; charset=utf-8");
include 'db.php' ;
// กำหนดค่าตัวแปร
$userID = $_POST['userID'];
$questionId = $_POST['questionId'];
try {
    

    // กำหนด query
    $sql = "INSERT INTO `log` (`userID`, `questionID`) VALUES (?, ?)";
    $stmt = $dbh->prepare($sql);

    // Bind parameters
    $stmt->bindParam(1, $userID);
    $stmt->bindParam(2, $questionId);

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