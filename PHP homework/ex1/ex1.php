<?php

$numbers = [1, 2, '3', 6, 2, 3, 2, 3];

$count = 0;

foreach ($numbers as $num) {
    if ($num === 3) {
        $count += 1;
    }
}

print "Found it $count times";
