//package main;
//
//import config.HsqlDataSource;
//import config.MvcConfig;
//import dao.OrderDao;
//import jakarta.servlet.ServletContext;
//import model.Order;
//import org.springframework.context.ConfigurableApplicationContext;
//import org.springframework.context.annotation.AnnotationConfigApplicationContext;
//
//public class Tester {
//
//    public static void main(String[] args) {
//
//        ConfigurableApplicationContext ctx =
//              new AnnotationConfigApplicationContext(
//                      MvcConfig.class, HsqlDataSource.class);
//
//        try (ctx) {
//
//            OrderDao dao = ctx.getBean(OrderDao.class);
//
//            Order newOrder = new Order("A345345"); // Populate the order details
//            dao.insertOrder(newOrder);
//
////            Order retrievedOrder = dao.findOrderById(newOrder.getId());
////            System.out.println(retrievedOrder);
//        }
//    }
//}