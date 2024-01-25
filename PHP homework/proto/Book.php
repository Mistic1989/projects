<?php

class Book {

    public int $id;
    public string $title;
    public int $grade;
    public string $isRead;
    public array $authors = [];

    /**
     * @param int $id
     * @param string $title
     * @param int $grade
     * @param string $isRead
     * @param array $authors
     */
    public function __construct(int $id, string $title, int $grade, string $isRead, array $authors)
    {
        $this->id = $id;
        $this->title = $title;
        $this->grade = $grade;
        $this->isRead = $isRead;
        $this->authors = $authors;
    }

    public function addAuthor($author): void {
        $this->authors[] = $author;
    }

}