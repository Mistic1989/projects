<?php

$data = urlencode($_POST['data']);

?>

<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Kinnitamise näide</title>
</head>
<body id="confirm-page">

<h4>Kas olete kindel, et soovite andmed salvestada?</h4>

<a href="." id="cancel">Tühista</a>

<a href="save.php?data=<?= $data ?>" id="confirm">Kinnita</a>

</body>
</html>
