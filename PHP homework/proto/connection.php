<?php

const USERNAME = 'web2023';
const PASSWORD = 'f21124';

function getConnection(): PDO {
    $host = 'db.mkalmo.eu';

    $address = sprintf('mysql:host=%s;port=3306;dbname=%s',
        $host, USERNAME);

    return new PDO($address, USERNAME, PASSWORD);
}

$dao = new Dao();