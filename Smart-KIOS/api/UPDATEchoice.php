<?php
header("Access-Control-Allow-Origin: *");
header("Content-type: application/json; charset=utf-8");
include 'db.php' ;
// กำหนดค่าตัวแปร
$input_data = json_decode(file_get_contents("php://input"), true);
$text = $_POST['text'];
$questionId = $_POST['questionId'];
$userID = $_POST['userID'];
echo json_encode(array('text' => $text));
echo json_encode(array('questionId' => $questionId));
echo json_encode(array('userID' => $userID));
try {
    

    // กำหนด query
    $sql = "UPDATE `log` SET `text`= (?) WHERE `questionID` = (?) AND `userID` = ? AND DATE(`date`) = CURDATE()";
    $stmt = $dbh->prepare($sql);

    // Bind parameters
    $stmt->bindParam(1, $text);
    $stmt->bindParam(2, $questionId);
    $stmt->bindParam(3, $userID);
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