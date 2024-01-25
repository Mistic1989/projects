<?php

$message = $_POST['message'] ?? '';

saveMessage($message);

include 'thanks.html';

//header('Location: thanks.html');

function saveMessage(string $message): void {
    // Some code to saves the message
    // This is not important in this context.
}


