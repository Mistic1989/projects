<?php

function getDaysUnderTempDictionary(float $targetTemp): array {

    require_once 'ex7.php';
    $inputFile = fopen(__DIR__ . '/data/temperatures-filtered.csv', "r");
    $result = array();
    while(! feof($inputFile)) {
        $input = fgetcsv($inputFile);
        if (!$input) {
            continue;
        }
        $year = intval($input[0]);
        if (!in_array($year, array_keys($result))) {
            $result += array($year=>getDaysUnderTemp($year, $targetTemp));
        }
    }

    return $result;
}

function dictToString(array $dict): string {
    $result = array();
    foreach ($dict as $key => $value) {
        $result[] = $key . ' => ' . $value;
    }
    return '[' . join(", ", $result) . ']';
}

//var_dump(getDaysUnderTempDictionary(-13));