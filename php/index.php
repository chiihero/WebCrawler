
<?php
$mysqli = new mysqli("139.199.11.57", "webcrawler", "webcrawler1", "webcrawler");
if(!$mysqli)  {
    echo"连接失败". "<br>";
}else{
    echo"连接成功". "<br>";
}
$result = $mysqli->query("SELECT * FROM picture_info order by id desc limit 5 ");
// 输出数据

//echo $result->error;
if ($result->num_rows > 0) {
    // 输出数据
    while($row = $result->fetch_assoc()) {
        echo  $row["name"].$row["link"]. "<br>";
    }
}
$mysqli->close();
?>