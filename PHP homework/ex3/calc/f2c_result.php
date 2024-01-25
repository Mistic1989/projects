<?php

require_once 'functions.php';

$input = $_POST['temperature'] ?? null;

if ($input === null || $input === '') {
    $message = 'Insert temperature';
} else if (!is_numeric($input)) {
    $message = 'Temperature must be an integer';
} else {
    $inputTemp = intval($input);

    $result = f2c($inputTemp);

    $message = sprintf("%d degrees in Fahrenheits is %d degrees in Celsius", $inputTemp, $result);
}

?>

<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Fahrenheit to Celsius</title>
</head>
<body>

    <nav>
        <a href="index.html" id="c2f">Celsius to Fahrenheit</a> |
        <a href="f2c.html" id="f2c">Fahrenheit to Celsius</a>
    </nav>

    <main>

        <h3>Fahrenheit to Celsius</h3>
        <em><?= $message ?></em>

    </main>

</body>
</html>