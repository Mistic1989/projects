<?php

class Post {

    public ?string $id = null;
    public string $title;
    public string $text;

    public function __construct(?string $id, string $title, string $text) {
        $this->id = $id;
        $this->title = $title;
        $this->text = $text;
    }

    public function __toString(): string {
        return sprintf('Id: %s, Title: %s, Text: %s',
            $this->id, $this->title, $this->text);
    }

}