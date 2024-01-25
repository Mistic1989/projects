package model;

import java.util.List;

public interface OrderDaoInterface {
    Order insertOrder(Order order);

    List<Order> findOrders();

    void deleteOrderById(Long id);

    Order findOrderById(Long id);

}
