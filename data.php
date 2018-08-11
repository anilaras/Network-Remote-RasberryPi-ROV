<?php
      // All form data is in $_POST
$TempDataFile = file_get_contents("./temp.dat", "r") or die("Unable to open file!");
//$ADCDataFile = file_get_contents("", "r") or die("Unable to open file!");
$i = "wasjdokjsakldj";

$arr = array('temp' => $TempDataFile, 'adcdata' => $i);
echo json_encode($arr);
?>