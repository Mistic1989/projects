<?php

$list = [1, 2, 3, 2, 6];

function isInList($list, $elementToBeFound): bool {
    foreach ($list as $element) {
        if ($element === $elementToBeFound) {
            return true;
        }
    }

    return false;
}