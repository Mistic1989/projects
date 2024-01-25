<?php

class Dao {

    private PDO $connection;

    public function __construct() {
        $this->connection = getConnection();
    }

    public function findBookById($id): array {

        $stmt = $this->connection->prepare('select title, books.grade as book_grade, isRead, book_author.id as book_author_id,
        authors.id as author_id, firstName, lastName, authors.grade as author_grade from books
        left join book_author on books.id = book_author.book_id
        left join authors on book_author.author_id = authors.id where book_id = :id');

        $stmt->bindValue(':id', $id);
        $stmt->execute();

        $result = [];
        foreach ($stmt as $item) {
            if (isset($result[$id])) {
                $author = new Author($item['author_id'], $item['book_author_id'], $item['firstName'], $item['lastName'], $item['author_grade']);
                $result[$id]->authors[] = $author;
            } else {
                $result[$id] = new Book($id, $item['title'], $item['book_grade'], $item['isRead'],
                              [new Author($item['author_id'], $item['book_author_id'], $item['firstName'],
                               $item['lastName'], $item['author_grade'])]);
            }
        }

        return $result;
    }

    public function findAuthorById($id): array {

        $stmt = $this->connection->prepare('select authors.id, book_author.id as book_author_id, firstName, lastName,
                                        grade from authors  left join book_author on book_author.author_id = authors.id;');
        $stmt->execute();

        foreach ($stmt as $row) {
            if ($row['id'] == $id) {
                return [new Author($id, $row['book_author_id'], $row['firstName'], $row['lastName'], $row['grade'])];
            }
        }
        return [];
    }

    function saveBookToDatabase($book): void {

        $stmt = $this->connection->prepare('INSERT INTO books (title, grade, isRead) 
                                  VALUES (:title, :grade, :isRead);');
        $stmt->bindValue(':title', $book->title);
        $stmt->bindValue(':grade', $book->grade);
        $stmt->bindValue(':isRead', $book->isRead);

        $stmt->execute();

        $book_id = $this->connection->lastInsertId();

        $stmt = $this->connection->prepare('INSERT INTO book_author (book_id, author_id) VALUES (:book_id, :author_id);');

        foreach ([$book->authors[0]->id, $book->authors[1]->id] as $author) {
            if ($author !== 0) {
                $stmt->bindValue(':book_id', $book_id);
                $stmt->bindValue(':author_id', $author);
                $stmt->execute();
            }
        }
    }

    function saveAuthorToDatabase($author): void {

        $stmt = $this->connection->prepare('INSERT INTO authors (firstName, lastName, grade)
                                  VALUES (:firstName, :lastName, :grade);');

        $stmt->bindValue(':firstName', $author->firstName);
        $stmt->bindValue(':lastName', $author->lastName);
        $stmt->bindValue(':grade', $author->grade);

        $stmt->execute();
    }

    function editAuthors($delete, $author): void {
        if ($delete === 'author-delete') {
            $stmt = $this->connection->prepare("delete from authors where id = :id");
            $stmt->bindValue(':id', $author->id);
        } else {
            $stmt = $this->connection->prepare('update authors set firstName = :firstName,
                 lastName = :lastName, grade = :grade where id = :id');
            $stmt->bindValue(':id', $author->id);
            $stmt->bindValue(':firstName', $author->firstName);
            $stmt->bindValue(':lastName', $author->lastName);
            $stmt->bindValue(':grade', $author->grade);
        }
        $stmt->execute();
    }

    function editBooks($delete, $book): void {

        if ($delete === 'book-delete') {
            $stmt = $this->connection->prepare("delete from books where id = :id");
            $stmt->bindValue(':id', $book->id);
            $stmt->execute();
        } else {

            $stmt = $this->connection->prepare('update books set title = :title,
                    grade = :grade, isRead = :isRead where id = :id');
            $stmt->bindValue(':id', $book->id);
            $stmt->bindValue(':title', $book->title);
            $stmt->bindValue(':grade', $book->grade);
            $stmt->bindValue(':isRead', $book->isRead);
            $stmt->execute();

            foreach ($book->authors as $author) {
                if ($author->id !== 0) {
                    $stmt = $this->connection->prepare('update book_author set author_id = :author_id where id = :book_author_id');
                    $stmt->bindValue(':book_author_id', $author->book_author_id);
                    $stmt->bindValue(':author_id', $author->id);
                    $stmt->execute();
                }
            }
        }
    }

    function getBooks(): array {

        $stmt = $this->connection->prepare('select books.id as id, authors.id as authors_id, book_author.id as book_author_id,
       title, firstName, lastName, books.grade as book_grade, authors.grade as author_grade, isRead from books left join book_author on books.id = book_author.book_id
                                                                                                       left join authors on book_author.author_id = authors.id');
        $stmt->execute();

        $result = [];
        foreach ($stmt as $item) {
            $id = $item['id'] ?? 0;
            $title = $item['title'];
            $author_id = $item['authors_id'] ?? 0;
            $book_author_id = $item['book_author_id'] ?? 0;
            $firstName = $item['firstName'] ?? '';
            $lastName = $item['lastName'] ?? '';
            $book_grade = $item['book_grade'] ?? 0;
            $author_grade = $item['author_grade'] ?? 0;
            $isRead = $item['isRead'] ?? 'off';
            if (isset($result[$id])) {
                $result[$id]->addAuthor(new Author($author_id, $book_author_id, $firstName, $lastName, $author_grade));
            } else {
                $result[$id] = new Book($id, $title, $book_grade, $isRead,
                    [new Author($author_id, $book_author_id, $firstName, $lastName, $author_grade)]);
            }
        }

        return $result;
    }

    function getAuthors(): array {

        $stmt = $this->connection->prepare('select book_author.id as book_author_id, authors.id as authors_id,
       authors.firstName, authors.lastName, authors.grade from authors left join book_author on book_author.id = authors.id');
        $stmt->execute();

        $result = [];
        foreach ($stmt as $item) {
            $book_author_id = $item['book_author_id'] ?? 0;
            $id = $item['authors_id'];
            $firstName = $item['firstName'];
            $lastName = $item['lastName'];
            $grade = $item['grade'];
            $result[] = new Author($id, $book_author_id, $firstName, $lastName, $grade);
        }

        return $result;
    }

    function validateAuthor($firstName, $lastName): array {

        $result = [];
        if (!(isset($firstName) && strlen($firstName) > 0 && strlen($firstName) < 22)) {
            $result[] = 'Eesnimi peab olema 1 kuni 21 märki!';
        }
        if (!(isset($lastName) && strlen($lastName) > 1 && strlen($lastName) < 23)) {
            $result[] = 'Perekonnanimi peab olema 2 kuni 22 märki!';
        }

        return $result;
    }

    function validateBook($title): array {
        if (!(isset($title) && strlen($title) > 2 && strlen($title) < 24)) {
            return ['Pealkiri peab olema 3 kuni 23 märki!'];
        }

        return [];
    }
}