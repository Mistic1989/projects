<?php

//ini_set('display_errors', '1');

function addBooks(): void
{
    $lines =  file('books.txt');
    foreach ($lines as $line) {
        $data = explode("|", $line);

        print "<tr>" . PHP_EOL;

        print "<td align='left' width='40%'>";

        print str_replace('\n',"\n", $data[0]);
        print "</td>" . PHP_EOL;

        print "<td width='10%'>";
        print $data[1];
        print "</td>" . PHP_EOL;

        print "</tr>" . PHP_EOL;
    }
}

function addAuthors(): void
{
    $lines =  file('authors.txt');
    foreach ($lines as $line) {
        $data = explode("|", $line);

        print "<tr>" . PHP_EOL;
        print "<td align='left' width='40%'>";

        print str_replace('\n',"\n", $data[0]);;
        print "</td>" . PHP_EOL;

        print "<td width='50%'>";
        print print str_replace('\n',"\n", $data[1]);;
        print "</td>" . PHP_EOL;

        print "<td width='10%'>";
        print $data[2];
        print "</td>" . PHP_EOL;

        print "</tr>" . PHP_EOL;
    }
}

$command = $_POST['submitButton'] ?? 'show-form';

$page = null;
if (isset($_GET['page'])) {
    $page = $_GET['page'];
}

if ($command === 'book-add') {
    $title = str_replace("\n", '\n', $_POST['title']);
    $grade = 0;
    $isRead = 'off';

    if (isset($_POST['grade'])) {
        $grade = $_POST['grade'];
    }
    if (isset($_POST['isRead']) && $_POST['isRead'] === 'on') {
        $isRead = $_POST['isRead'];
    }

    $books = fopen("books.txt", "a");
    fputcsv($books, [$title, $grade, $isRead], "|");
    fclose($books);

    include 'books.php';
}
else if ($command === 'author-add') {
    $firstName = str_replace("\n", '\n', $_POST['firstName']);
    $lastName = str_replace("\n", '\n', $_POST['lastName']);
    $grade = 0;

    if (isset($_POST['grade'])) {
        $grade = $_POST['grade'];
    }

    $authors = fopen("authors.txt", "a");
    fputcsv($authors, [$firstName, $lastName, $grade], "|");
    fclose($authors);

    include 'author-list.php';
}
else if (($command === 'show-form' && $page === 'book-list') || ($command === 'show-form' && !$page)) {
    include 'books.php';
}
else if ($command === 'show-form' && $page == 'book-form') {
    include 'book-add.php';
}
else if ($command === 'show-form' && $page == 'author-list') {
    include 'author-list.php';
}
else if ($command === 'show-form' && $page == 'author-form') {
    include 'author-add.php';
}
else {
    throw new Error('unknown command: ' . $command);
}