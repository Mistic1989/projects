<?php

ini_set('display_errors', '1');

require_once '../ex1/ex7.php';
require_once '../ex2/functions.php';

$command = $_POST['command'] ?? 'show-form';

if ($command === 'show-form' && !isset($_GET['page'])) {
    include 'pages/days-under-temp.php';
}
else if ($command === 'days-under-temp') {
    $year = $_POST['year'];
    $temp = $_POST['temp'];
    $message = getDaysUnderTemp($year, $temp);

    include 'pages/result.php';

} else if ($command === 'avg-winter-temp') {
    $year = $_POST['year'];
    $message = getAverageWinterTemp($year);
    include 'pages/result.php';
}
else if (isset($_GET['page']) && $_GET['page'] === 'avg-winter-temp') {
    include 'pages/avg-winter-temp.php';
}
else if (isset($_GET['page']) && $_GET['page'] === 'days-under-temp') {
    include 'pages/days-under-temp.php';
}

else {
    throw new Error('unknown command: ' . $command);
}
