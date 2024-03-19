<?php
header("Access-Control-Allow-Origin: *");
header("Content-type: application/json; charset=utf-8");
include 'db.php' ;
// กำหนดค่าตัวแปร
$studentID = $_POST['studentID'];
$name = $_POST['name'];
$lastname = $_POST['lastname'];
$role = $_POST['role'];
try {
    

    // กำหนด query
    $sql = "INSERT INTO `user`(`studentID`,`name`, `lastname`, `role`) VALUES (?,?,?,?)";
    $stmt = $dbh->prepare($sql);

    // Bind parameters
    $stmt->bindParam(1, $studentID);
    $stmt->bindParam(2, $name);
    $stmt->bindParam(3, $lastname);
    $stmt->bindParam(4, $role);

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