<?php

function getAverageWinterTemp(int $targetYear): float {
    $inputFile = fopen("../ex1/data/temperatures-filtered.csv", "r");
    $result = 0.0;
    $days_count = 0;

    while(! feof($inputFile)) {
        $dict = fgetcsv($inputFile);

        if (!$dict) {
            continue;
        }
        $year = intval($dict[0]);
        $month = intval($dict[1]);
        $temp = floatval($dict[4]);

        if ($targetYear === $year && ($month === 1 || $month === 2 || $month === 12)) {
            $days_count += 1;
            $result += $temp;
        }
    }
    fclose($inputFile);

    return round($result / $days_count, 2);
}
