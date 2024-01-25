<?php

$input = '[1, 4, 2, 0]';

function stringToIntegerList(string $input): array {
    $input = str_replace($input[0], "", $input);
    $input = str_replace($input[strlen($input) - 1], "", $input);
    $split = explode(",", $input);
    $result = array();
    foreach ($split as $num) {
        $result[] = intval($num);
    }
    return $result;
}