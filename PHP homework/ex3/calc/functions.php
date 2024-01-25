<?php

print c2f(20) . PHP_EOL;
print f2c(68) . PHP_EOL;

function c2f($temp) {
    return intval($temp) * 9/5 + 32;
}

function f2c($temp) {
    return (intval($temp) - 32) / (9/5);
}

