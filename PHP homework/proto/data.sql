show databases;

use web2023;

show tables;

CREATE TABLE items (id INTEGER PRIMARY KEY, text VARCHAR(255));

# CREATE TABLE books (id INTEGER PRIMARY KEY AUTO_INCREMENT, title VARCHAR(255),
#                     grade INTEGER, isRead VARCHAR(255), author_id INTEGER);
#
# CREATE TABLE authors (id INTEGER PRIMARY KEY AUTO_INCREMENT, firstName VARCHAR(255),
#                       lastName VARCHAR(255), grade INTEGER);

CREATE TABLE books (id INTEGER PRIMARY KEY AUTO_INCREMENT, title VARCHAR(255),
                    grade INTEGER, isRead VARCHAR(255), author_id INTEGER);

CREATE TABLE authors (id INTEGER PRIMARY KEY AUTO_INCREMENT, firstName VARCHAR(255),
                      lastName VARCHAR(255), grade INTEGER);

CREATE TABLE book_author (id INTEGER PRIMARY KEY AUTO_INCREMENT, book_id integer not null, author_id integer not null);

# CREATE TABLE book_author (book_id integer not null, author_id integer not null,
#                           foreign key (book_id) references books(id) ON DELETE CASCADE,
#                           foreign key (author_id) references authors(id) ON DELETE CASCADE);

select * from books left join book_author on books.id = book_author.book_id
                    left join authors on book_author.author_id = authors.id;

select * from books left join book_author on books.id = book_author.book_id
                    left join authors on book_author.author_id = authors.id where book_id = 4;

SELECT * from authors left join book_author on authors.id = book_author.id;

select b.id, title, b.grade, isRead, b.author_id from books b
left join authors a on a.id;

select * from books left join authors on books.author_id = authors.id;

select book_author.id as book_author_id, authors.id as author_id, authors.firstName, authors.lastName, authors.grade from authors
                                       left join book_author on book_author.author_id = authors.id;

DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS authors;
DROP TABLE IF EXISTS book_author;

select * from books left join book_author on books.id = book_author.book_id
                    left join authors on book_author.author_id = authors.id where book_id = :id;

select * from books left join book_author on books.id = book_author.book_id
                    left join authors on book_author.author_id = authors.id;

select books.id as id, authors.id as authors_id, book_author.id as book_author_id,
       title, firstName, lastName, books.grade as book_grade, authors.grade as author_grade, isRead from books left join book_author on books.id = book_author.book_id
                                                                                                       left join authors on book_author.author_id = authors.id;

select * from books left join book_author on books.id = book_author.book_id
                    left join authors on book_author.author_id = authors.id where book_id = :id;

select book_author.id as book_author_id, authors.id as authors_id,
       authors.firstName, authors.lastName, authors.grade from authors
                                                                   left join book_author on book_author.author_id = authors.id;

SELECT book_author.id as book_author_id, authors.id as authors_id,
       authors.firstName, authors.lastName, authors.grade from authors left join book_author on book_author.id = authors.id;

select * from books left join book_author on books.id = book_author.book_id
                    left join authors on book_author.author_id = authors.id where book_id = :id;