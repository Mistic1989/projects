package dao;

import jakarta.persistence.EntityManager;
import jakarta.persistence.NoResultException;
import jakarta.persistence.PersistenceContext;
import jakarta.persistence.TypedQuery;
import org.springframework.stereotype.Repository;
import user.User;

import java.util.List;

@Repository
public class UserDao {

    @PersistenceContext
    private EntityManager em;

    public User getUser(String username) {
        TypedQuery<User> query = em.createQuery(
                "select u from User u where u.username = :username",
                User.class);

        query.setParameter("username", username);

        try {
            return query.getSingleResult();
        } catch (NoResultException e) {
            return null;
        }
    }

    public List<User> findUsers() {

        return em.createQuery("select u from User u")
                .getResultList();
    }
}
