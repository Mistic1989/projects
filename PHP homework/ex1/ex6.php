<?php

$inputFile = fopen("data/temperatures-sample.csv", "r");
$outputFile = fopen("temperatures-filtered.csv", "w");

while(! feof($inputFile)) {
    $dict = fgetcsv($inputFile);

    if (!$dict || !is_numeric($dict[0])) {
        continue;
    }

    $year = intval($dict[0]);
    $month = $dict[1];
    $day = $dict[2];
    $hour = $dict[3];
    $temperature = $dict[9];

    if ($year > 2004) {
        fputcsv($outputFile, [$year, $month, $day, $hour, $temperature]);
    }
}

fclose($inputFile);
fclose($outputFile);