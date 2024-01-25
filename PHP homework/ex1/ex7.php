<?php

function getDaysUnderTemp(int $targetYear, float $targetTemp): float {
    $inputFile = fopen(__DIR__ . "/data/temperatures-filtered.csv", "r");
    $result = 0;

    while(! feof($inputFile)) {
        $dict = fgetcsv($inputFile);

        if (!$dict) {
            continue;
        }
        $year = intval($dict[0]);
        $temperature = floatval($dict[4]);

        if ($targetYear === $year && $temperature <= $targetTemp) {
            $result += 1;
        }
    }
    fclose($inputFile);

    return round($result / 24, 2);
}