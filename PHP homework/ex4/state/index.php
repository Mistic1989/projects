<?php

include 'functions.php';

$list1 = isset($_GET['list1_state'])
    ? unserialize(urldecode($_GET['list1_state']))
    : [1, 2, 3, 4];
$list2 = isset($_GET['list2_state'])
    ? unserialize(urldecode($_GET['list2_state']))
    : [5, 6];

if (isset($_GET['list1_to_list2'])) {
    $value = $_GET['list1'];
    $list1 = removeElementByValue($value, $list1);
    $list2[] = $value;
}

if (isset($_GET['list2_to_list1'])) {
    $value = $_GET['list2'];
    $list2 = removeElementByValue($value, $list2);
    $list1[] = $value;
}

$list1state = urlencode(serialize($list1));
$list2state = urlencode(serialize($list2));

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Rakenduse seisu hoidmine</title>
</head>
<body>

<form>

    <input type="text" name="list1_state" value="<?= $list1state ?>">
    <input type="text" name="list2_state" value="<?= $list2state ?>">

    <select name="list1" multiple="multiple">
        <?php foreach ($list1 as $number): ?>
            <option value="<?= $number ?>"><?= $number ?></option>
        <?php endforeach; ?>
    </select>

    <button type="submit" name="list1_to_list2">&gt;&gt;</button>
    <button type="submit" name="list2_to_list1">&lt;&lt;</button>

    <select name="list2" multiple="multiple">
        <?php foreach ($list2 as $number): ?>
            <option value="<?= $number ?>"><?= $number ?></option>
        <?php endforeach; ?>
    </select>

</form>

</body>
</html>
