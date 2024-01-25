<?php

//$sets = distributeToSets([1, 2, 1]);
//
//var_dump($sets);

function distributeToSets(array $input): array {

    $sets = [];
    foreach ($input as $item) {
        if (isset($sets[$item])) {
            $sets[$item][] = $item;
        } else {
            $sets[$item] = [$item];
        }
   }
   return $sets;
}
