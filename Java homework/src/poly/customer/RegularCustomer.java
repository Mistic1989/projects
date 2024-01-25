package poly.customer;

import java.time.LocalDate;

public final class RegularCustomer extends AbstractCustomer {


    public RegularCustomer(String id, String name,
                           int bonusPoints, LocalDate lastOrderDate) {

        super(id, name, bonusPoints);
        this.lastOrderDate = lastOrderDate;
    }

    @Override
    public void collectBonusPointsFrom(Order order) {
        LocalDate orderDate = order.getDate();
        orderDate = orderDate.minusMonths(1);

        if (!lastOrderDate.isAfter(orderDate) && order.getTotal() >= 100) {
            this.bonusPoints = Double.valueOf(order.getTotal() + getBonusPoints()).intValue();
        }

        if (lastOrderDate.isAfter(orderDate) && order.getTotal() >= 100) {
            this.bonusPoints = Double.valueOf((order.getTotal() + getBonusPoints()) * 1.5).intValue();
        }
    }

    public String getCustomerType() {
        return CustomerType.REGULAR.toString();
    }
}