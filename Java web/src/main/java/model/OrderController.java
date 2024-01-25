package model;

import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
public class OrderController {

    private OrderDaoInterface dao;

    public OrderController(OrderDaoInterface dao) {
        this.dao = dao;
    }

    @GetMapping("orders")
    public List<Order> getOrders() {
        return dao.findOrders();
    }

    @GetMapping("orders/{id}")
    public Order getOrderById(@PathVariable Long id) {
        return dao.findOrderById(id);
    }

    @PostMapping("orders")
    @ResponseStatus(HttpStatus.CREATED)
    public Order save(@RequestBody @Valid Order order) {
        return dao.insertOrder(order);
    }

    @DeleteMapping("orders/{id}")
    public void deleteOrder(@PathVariable Long id) {
        dao.deleteOrderById(id);
    }
}
