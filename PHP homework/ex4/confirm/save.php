<?php

saveData($_GET['data']);

// redirect to index.php passing message about success or failure
header('Location: index.php?message=success');

function saveData(string $data) {
    // log to server console (for debugging)
    error_log('Saving data: ' . $data);

    // actual saving is not important in this context
}