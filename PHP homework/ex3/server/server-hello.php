<?php

$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
socket_bind($socket, "127.0.0.1", "8080");
socket_listen($socket);

print "Server is running...";

while (true) {
    $acceptedSocket = socket_accept($socket);

    $response = "HTTP/1.1 200 OK\nContent-Length: 6\n\nHello!";

    socket_write($acceptedSocket, $response);
}
