<?php

class Post {

    public string $title;
    public string $text;

    public function __construct(string $title, string $text) {
        $this->title = $title;
        $this->text = $text;
    }

    public function __toString(): string {
        return sprintf('{ Title: %s, Text: %s }', $this->title, $this->text);
    }
}