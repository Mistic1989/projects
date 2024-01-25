
insert into orders (order_number) VALUES ('A6823sc55');
insert into orderrows (itemName, quantity, price, orderid) VALUES ('asdf', 5, 43, 14);

-- select * from order left join orderrows on order.id = orderrows.postId order by orderrows.postId;
select * from order left join orderrows on order.id = orderrows.postId where order.id = ? and orderrows is not null;

select order.id as post_id, ordernumber, orderrows.id as orderrows_id,
       itemname, quantity, price, postid from order left join orderrows on order.id = orderrows.postId;

select * from order left join orderrows on order.id = orderrows.postId;

delete from order where order.id = ?;

select * from order;


select order.id as post_id, ordernumber, orderrows.id as orderrows_id, itemname, quantity, price,
       postid from order left join orderrows on order.id = orderrows.postId;

INSERT INTO USERS (username, password, enabled, first_name)
VALUES ('user', '$2a$10$qkk9P/EZtVrwQl306efA0eecZDlrXU6xG.Q24gnfRKCTYP6eY4RW6', true, 'Jack');

INSERT INTO USERS (username, password, enabled, first_name)
VALUES ('admin', '$2a$10$Xv77YLPw237L.iHXE4Yzde1oQOajoZml7aRXiiSc0AhhCBJI.gepm', true, 'Jill');
INSERT INTO AUTHORITIES (username, authority) VALUES ('user', 'ROLE_USER');
INSERT INTO AUTHORITIES (username, authority) VALUES ('admin', 'ROLE_ADMIN');

