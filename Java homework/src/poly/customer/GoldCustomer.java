package poly.customer;

public final class GoldCustomer extends AbstractCustomer {

    public GoldCustomer(String id, String name, int bonusPoints) {
        super(id, name, bonusPoints);
    }

    @Override
    public void collectBonusPointsFrom(Order order) {
        if (order.getTotal() >= 100) {
            this.bonusPoints = Double.valueOf((order.getTotal() + this.getBonusPoints()) * 1.5).intValue();
        }
    }

    public String getCustomerType() {
        return CustomerType.GOLD.toString();
    }
}