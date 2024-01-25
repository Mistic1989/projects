package dao;

import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.persistence.TypedQuery;
import jakarta.transaction.Transactional;
import model.Order;
import model.OrderDaoInterface;

import org.springframework.stereotype.Repository;

import java.util.List;


@Repository
public class OrderDao implements OrderDaoInterface {

    @PersistenceContext
    private EntityManager em;

    @Override
    public void deleteOrderById(Long id) {

        Order order = em.find(Order.class, id);

        if (order != null) {
            em.remove(order);
        }
    }

    @Override
    public Order findOrderById(Long id) {

        TypedQuery<Order> query = em.createQuery(
                "select o from Order o where o.id = :id",
                Order.class);

        query.setParameter("id", id);
        return query.getSingleResult();
    }

    @Override
    public List<Order> findOrders() {

        return em.createQuery("select o from Order o")
                .getResultList();
    }

    @Override
    @Transactional
    public Order insertOrder(Order order) {

        if (order.getId() == null) {
            em.persist(order);
        } else {
            em.merge(order);
        }

        return order;
    }
}