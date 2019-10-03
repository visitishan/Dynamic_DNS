<?php
if(isset($_GET['ip'])){
    $txt = $_GET['ip'].",";
    $myfile = file_put_contents('addr.txt', $txt.PHP_EOL , FILE_APPEND | LOCK_EX);
    echo "Success";
}else{
    $myfileContents = file_get_contents("addr.txt");
    $myfileContents = explode(",",$myfileContents);
    if($myfileContents[count($myfileContents)-1] != ""){
        $address = $myfileContents[count($myfileContents)-2];
    }else{
        $address = $myfileContents[count($myfileContents)-1];
    }
    header('Location: '.'http://'.$address);
}
?>