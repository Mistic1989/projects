<?php

require_once 'Post.php';
require_once 'ex3.php';

const DATA_FILE = 'data/posts.txt';

function getAllPosts(): array {
    $lines = file(DATA_FILE);
    $result = [];
    foreach ($lines as $item) {
        $split = explode(";", trim($item));
        $result[] = new Post(urldecode($split[0]), urldecode($split[1]));
    }
    return $result;
}

function savePost(Post $post): void {
    $result = urlencode($post->title) . ';' . urlencode($post->text) . PHP_EOL;
    file_put_contents(DATA_FILE, $result, FILE_APPEND);
}