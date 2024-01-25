<?php

class Author {

    public int $id;
    public int $book_author_id;
    public string $firstName;
    public string $lastName;
    public int $grade;

    /**
     * @param int $id
     * @param int $book_author_id
     * @param string $firstName
     * @param string $lastName
     * @param int $grade
     */
    public function __construct(int $id, int $book_author_id, string $firstName, string $lastName, int $grade)
    {
        $this->id = $id;
        $this->book_author_id = $book_author_id;
        $this->firstName = $firstName;
        $this->lastName = $lastName;
        $this->grade = $grade;
    }
}