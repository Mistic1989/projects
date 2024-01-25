<?php

require_once '../ex1/ex7.php'; // use existing code
require_once '../ex1/ex8.php';
require_once 'functions.php'; // separate functions from main program

$opts = getopt('c:y:t:', ['command:', 'year:', 'temp:']);

$command = $opts['command'] ?? null;

if ($command === 'days-under-temp' && array_key_exists('year', $opts) && array_key_exists('temp', $opts)) {
    print getDaysUnderTemp($opts['year'], $opts['temp']);

} else if ($command === 'days-under-temp-dict' && array_key_exists('temp', $opts)) {
    print dictToString(getDaysUnderTempDictionary($opts['temp']));

} else if ($command === 'avg-winter-temp' && array_key_exists('year', $opts)) {
    print getAverageWinterTemp(intval($opts['year']));

} else {
    showError('command is missing or is unknown');
}

function showError(string $message): void {
    fwrite(STDERR, $message . PHP_EOL);
    exit(1);
}