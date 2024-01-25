<?php

    $messages = [
            'success' => 'Andmed salvestatud!',
            'error' => 'Viga salvestamisel!',
        ];

    $messageKey = $_GET['message'] ?? null;
    $message = $messages[$messageKey] ?? null;

?>

<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Kinnitamise näide</title>
</head>
<body id="form-page">

<?php if ($message): ?>
<h3 id="message-success">
    <?= $message ?>
</h3>
<?php endif; ?>

<br>

<form method="post" action="confirm.php">
    <label for="ta">Andmed:</label>

    <input id="ta" name="data" />

    <button name="sendButton" type="submit">Salvesta</button>
</form>

</body>
</html>
