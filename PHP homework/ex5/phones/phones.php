<?php

require_once '../connection.php';
require_once 'Contact.php';

$contacts = getContacts();

//var_dump($contacts);
//foreach ($contacts as $contact) {
//    print $contact;
//}

function getContacts(): array {
    $conn = getConnection();

    $stmt = $conn->prepare('SELECT id, name, number
                        from contact c
                        left join phone p on c.id = p.contact_id');

    $stmt->execute();

    $contacts = [];
    foreach ($stmt as $row) {
        $id = $row['id'];
        $number = $row['number'];
        $name = $row['name'];


        if (isset($contacts[$id])) {
            $contact = $contacts[$id];

        } else {
            $contact = new Contact($id, $name);
            $contacts[$id] = $contact;
        }

        if ($number !== null) {
            $contact->addPhone($number);
        }

//        var_dump($id);
//        var_dump($name);
//        var_dump($number);
    }

    return array_values($contacts);
}