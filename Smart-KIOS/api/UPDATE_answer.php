<?php
header("Access-Control-Allow-Origin: *");
header("Content-type: application/json; charset=utf-8");
include 'db.php' ;
// กำหนดค่าตัวแปร
$text = $_POST['text'];
$answerid = $_POST['answerid'];
echo json_encode(array('text' => $text));
echo json_encode(array('questionId' => $answerid));
try {
    

    // กำหนด query
    $sql = "UPDATE `answer` SET `answerTEXT`= ? WHERE `answerID` = ? ";
    $stmt = $dbh->prepare($sql);

    // Bind parameters
    $stmt->bindParam(1, $text);
    $stmt->bindParam(2, $answerid);

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