<?php

require_once 'proto/vendor/tpl.php';
require_once 'proto/Book.php';
require_once 'proto/Author.php';

$command = $_POST['submitButton'] ?? null;
$navigate = $_GET['command'] ?? null;
$delete = $_POST['deleteButton'] ?? null;
$getId = null;

if ($navigate !== 'book-form' || $navigate !== 'author-form') {
    require_once 'proto/Dao.php';
    require_once 'proto/connection.php';
}

if (isset($command)) {
    $getId = explode("=", $command) ?? null;
}
if (isset($delete)) {
    $delete = explode("=", $delete) ?? null;
}

if ((isset($getId) && $getId[0] === 'author-edit') || (isset($delete) && $delete[0] === 'author-delete')) {

    $id = $getId[1] ?? null;
    if ($delete !== null && $delete[0] === 'author-delete') {
        $id = $delete[1];
    }

    if (count($dao->validateAuthor($_POST['firstName'], $_POST['lastName'])) === 0) {

        $firstName = trim($_POST['firstName']);
        $lastName = trim($_POST['lastName']);
        $grade = $_POST['grade'] ?? 0;

        if (isset($delete)) {
            $delete = $delete[0];
        }
        $dao->editAuthors($delete, new Author($id, 0, $firstName, $lastName, $grade));

        if ($delete === 'author-delete') {
            header('Location: ?command=author-list&message=deleted');
        }
        if ($delete === null) {
            header('Location: ?command=author-list&message=updated');
        }
    } else {
        header('Location: ?command=author-edit&id=' . $id);
    }
}

if ((isset($getId) && $getId[0] === 'book-edit') || (isset($delete) && $delete[0] === 'book-delete')) {

    $id = $getId[1] ?? null;
    $result = $dao->findBookById($id)[$id] ?? [];
    $book_author_id1 = $result->authors[0]->book_author_id ?? 0;
    $book_author_id2 = $result->authors[1]->book_author_id ?? 0;

    if ($delete !== null && $delete[0] === 'book-delete') {
        $id = $delete[1];
    }
    $author_id = $_POST['author1'] ?? null;
    $author_id2 = $_POST['author2'] ?? null;

    if (count($dao->validateBook($_POST['title'])) === 0) {

        $title = trim($_POST['title']);
        $isRead = $_POST['isRead'] ?? 'off';
        $grade = $_POST['grade'] ?? 0;

        if (isset($delete)) {
            $delete = $delete[0];
        }

        if ($author_id == '') {
            $author_id = 0;
        }

        if ($author_id2 == '') {
            $author_id2 = 0;
        }

        $dao->editBooks($delete, new Book($id, $title, $grade, $isRead,
        [new Author($author_id ?? 0, $book_author_id1 ?? 0, '', '', 0),
         new Author($author_id2 ?? 0, $book_author_id2 ?? 0, '', '', 0)]));

        if ($delete === 'book-delete') {
            header('Location: ?command=book-list&message=deleted');
        }
        if ($delete === null) {
            header('Location: ?command=book-list&message=updated');
        }
    } else {
        header('Location: ?command=book-edit&id=' . $id);
    }
}

if ($command === 'book-add') {

    $validate = $dao->validateBook($_POST['title']);

    if (count($validate) === 0) {
        $author_id = $_POST['author1'] ?? 0;
        $author_id2 = $_POST['author2'] ?? 0;

        if (!is_numeric($_POST['author1'])) {
            $author_id = 0;
        }
        if (!is_numeric($_POST['author2'])) {
            $author_id2 = 0;
        }
        $title = $_POST['title'];
        $grade = 0;
        if (isset($_POST['grade']) && is_numeric($_POST['grade'])) {
            $grade = $_POST['grade'];
        }

        $isRead = $_POST['isRead'] ?? 'off';

        $dao->saveBookToDatabase(new Book(0, $title, $grade, $isRead,
        [new Author($author_id, 0, '', '', 0), new Author($author_id2, 0, '', '', 0)]));

        header('Location: ?command=book-list&message=saved');
    } else {
        $author_id = '';
        $author_id2 = '';
        $firstName = '';
        $lastName = '';
        $firstName2 = '';
        $lastName2 = '';
        $deleteVisible = false;
        $submitValue = 'book-add';
        $title = $_POST['title'] ?? '';
        $grade = $_POST['grade'] ?? '';
        $isRead = $_POST['isRead'] ?? '';
        $message = $validate;

        if ($isRead === 'on') {
            $isRead = 'checked';
        } else {
            $isRead = '';
        }

        $data = [
            'author_id' => $author_id,
            'author_id2' => $author_id2,
            'firstName' => $firstName,
            'lastName' => $lastName,
            'firstName2' => $firstName2,
            'lastName2' => $lastName2,
            'title' => $title,
            'grade' => $grade,
            'isRead' => $isRead,
            'message' => $message,
            'submitValue' => $submitValue,
            'deleteVisible' => $deleteVisible,
            'authors' => $dao->getAuthors(),
            'contentPath' => 'book-add.html',
            'menu' => 'menu.html',
            'footer' => 'footer.html',
            'body' => 'book-form-page'
        ];

        print renderTemplate('proto/tpl/main.html', $data);

    }
}

else if ($command === 'author-add') {

    $validate = $dao->validateAuthor($_POST['firstName'], $_POST['lastName']);

    if (count($validate) === 0) {

        $firstName = $_POST['firstName'];
        $lastName = $_POST['lastName'];
        $grade = 0;

        $grade = isset($_POST['grade']) && is_numeric($_POST['grade']) ? $_POST['grade'] : 0;

        $dao->saveAuthorToDatabase(new Author(0, 0, $firstName, $lastName, $grade));

        header('Location: ?command=author-list&message=saved');
    } else {
        $deleteVisible = false;
        $submitValue = 'author-add';
        $firstName = $_POST['firstName'] ?? '';
        $lastName = $_POST['lastName'] ?? '';
        $grade = $_POST['grade'] ?? '';
        $message = $validate;

        $data = [
            'firstName' => $firstName,
            'lastName' => $lastName,
            'grade' => $grade,
            'message' => $message,
            'submitValue' => $submitValue,
            'deleteVisible' => $deleteVisible,
            'contentPath' => 'author-add.html',
            'menu' => 'menu.html',
            'footer' => 'footer.html',
            'body' => 'author-form-page'
        ];

        print renderTemplate('proto/tpl/main.html', $data);

    }

}
else if ($navigate === 'book-edit') {

    $deleteVisible = true;
    $id = $_GET['id'];

    $result = $dao->findBookById($id)[$id] ?? [];

    $title = $result->title ?? '';
    $grade = $result->grade ?? '';
    $isRead = $result->isRead ?? false;
    if ($isRead === 'on') {
        $isRead = true;
    } else {
        $isRead = false;
    }

    $firstName = $result->authors[0]->firstName ?? '';
    $lastName = $result->authors[0]->lastName ?? '';
    $firstName2 = $result->authors[1]->firstName ?? '';
    $lastName2 = $result->authors[1]->lastName ?? '';
    $author_id = $result->authors[0]->id ?? '';
    $author_id2 = $result->authors[1]->id ?? '';

    $deleteValue = 'book-delete=' . $id;
    $submitValue = 'book-edit=' . $id;

    $message = '';

    $data = [
        'author_id' => $author_id,
        'author_id2' => $author_id2,
        'firstName' => $firstName,
        'lastName' => $lastName,
        'firstName2' => $firstName2,
        'lastName2' => $lastName2,
        'title' => $title,
        'grade' => $grade,
        'isRead' => $isRead,
        'message' => $message,
        'deleteValue' => $deleteValue,
        'submitValue' => $submitValue,
        'deleteVisible' => $deleteVisible,
        'authors' => $dao->getAuthors(),
        'contentPath' => 'book-add.html',
        'menu' => 'menu.html',
        'footer' => 'footer.html',
        'body' => 'book-form-page'
    ];

    print renderTemplate('proto/tpl/main.html', $data);

}

else if ($navigate === 'author-edit') {

    $deleteVisible = true;
    $id = $_GET['id'];
    $deleteValue = 'author-delete';
    $submitValue = 'author-edit';
    $result = $dao->findAuthorById($id);

    $firstName = $result[0]->firstName ?? '';
    $lastName = $result[0]->lastName ?? '';
    $grade = $result[0]->grade ?? '';

    $message = '';

    $data = [
        'id' => $id,
        'firstName' => $firstName,
        'lastName' => $lastName,
        'grade' => $grade,
        'message' => $message,
        'submitValue' => $submitValue,
        'deleteVisible' => $deleteVisible,
        'contentPath' => 'author-add.html',
        'menu' => 'menu.html',
        'footer' => 'footer.html',
        'body' => 'author-form-page'
    ];

    print renderTemplate('proto/tpl/main.html', $data);

}
else if ($navigate === 'book-list' || $navigate === null) {
    $message = $_GET['message'] ?? '';

    if ($message === 'saved') {
        $message = 'Lisatud';
    }
    if ($message === 'deleted') {
        $message = 'Kustutatud';
    }
    if ($message === 'updated') {
        $message = 'Uuendatud';
    }

    $data = [
        'books' => $dao->getBooks(),
        'contentPath' => 'books.html',
        'menu' => 'menu.html',
        'body' => 'book-list-page',
        'footer' => 'footer.html',
        'message' => $message
    ];

    print renderTemplate('proto/tpl/main.html', $data);

}
else if ($navigate === 'book-form') {
    $author_id = '';
    $author_id2 = '';
    $firstName = '';
    $lastName = '';
    $firstName2 = '';
    $lastName2 = '';
    $title = '';
    $grade = '';
    $isRead = false;
    $message = [];
    $submitValue = 'book-add';
    $deleteVisible = false;

    $data = [
        'author_id' => $author_id,
        'author_id2' => $author_id2,
        'firstName' => $firstName,
        'lastName' => $lastName,
        'firstName2' => $firstName2,
        'lastName2' => $lastName2,
        'title' => $title,
        'grade' => $grade,
        'isRead' => false,
        'message' => $message,
        'submitValue' => $submitValue,
        'deleteVisible' => false,
        'authors' => $dao->getAuthors(),
        'contentPath' => 'book-add.html',
        'menu' => 'menu.html',
        'footer' => 'footer.html',
        'body' => 'book-form-page'
    ];

    print renderTemplate('proto/tpl/main.html', $data);

}
else if ($navigate === 'author-list') {
    $message = $_GET['message'] ?? '';

    if ($message === 'saved') {
        $message = 'Lisatud';
    }
    if ($message === 'deleted') {
        $message = 'Kustutatud';
    }
    if ($message === 'updated') {
        $message = 'Uuendatud';
    }

    $data = [
        'message' => $message,
        'contentPath' => 'author-list.html',
        'menu' => 'menu.html',
        'body' => 'author-list-page',
        'footer' => 'footer.html',
        'authors' => $dao->getAuthors()
    ];

    print renderTemplate('proto/tpl/main.html', $data);

}
else if ($navigate === 'author-form') {
    $firstName = '';
    $lastName = '';
    $grade = '';
    $message = [];
    $submitValue = 'author-add';
    $deleteVisible = false;

    $data = [
        'firstName' => $firstName,
        'lastName' => $lastName,
        'grade' => $grade,
        'message' => $message,
        'submitValue' => $submitValue,
        'deleteVisible' => false,
        'contentPath' => 'author-add.html',
        'menu' => 'menu.html',
        'footer' => 'footer.html',
        'body' => 'author-form-page'
    ];

    print renderTemplate('proto/tpl/main.html', $data);

}
else {
    throw new Error('unknown command: ' . $command);
}