<?php

$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
socket_bind($socket, '127.0.0.1', '8080');
socket_listen($socket);

print 'Server is running...';

while (true) {
    $acceptedSocket = socket_accept($socket);

    $content = shell_exec('php ../multiplication/main.php');

    $response = addHeader($content);

    socket_write($acceptedSocket, $response);
}

function addHeader($content): string {
    $template = "HTTP/1.1 200 OK
                 Host: localhost:8080
                 Content-Type: text/html; charset=UTF-8
                 Content-Length: %d
                 
                 %s";

    $template = preg_replace('/^ +/m', '', $template);

    return sprintf($template, strlen($content), $content);
}
