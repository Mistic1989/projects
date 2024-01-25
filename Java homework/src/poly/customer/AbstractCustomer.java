package poly.customer;

import java.time.LocalDate;
import java.util.Objects;

public abstract sealed class AbstractCustomer
        permits GoldCustomer, RegularCustomer {

    protected LocalDate lastOrderDate;
    protected String id;
    protected String name;
    protected int bonusPoints;

    enum CustomerType {REGULAR, GOLD}

    public AbstractCustomer(String id, String name, int bonusPoints) {
        this.id = id;
        this.name = name;
        this.bonusPoints = bonusPoints;
    }

    public abstract void collectBonusPointsFrom(Order order);
    public abstract String getCustomerType();

    /**
     * Provides string representation of the object.
     * This string can be used for storing the object in text fail
     * @return string representation of the object.
     */

    public String getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public Integer getBonusPoints() {
        return bonusPoints;
    }

    public LocalDate getLastOrderDate() {
        return lastOrderDate;
    }

    @Override
    public boolean equals(Object obj) {
        if (obj == null || this.getClass() != obj.getClass()) {
            return false;
        }

        AbstractCustomer other = (AbstractCustomer) obj;
        boolean result = Objects.equals(id, other.id) &&
                Objects.equals(name, other.name) &&
                Objects.equals(bonusPoints, other.bonusPoints);

        if (this.getCustomerType().equals("REGULAR")) {
            return result && Objects.equals(lastOrderDate, other.lastOrderDate);
        }

        return result;
    }

    @Override
    public int hashCode() {
        if (Objects.equals(getCustomerType(), "REGULAR")) {
            return Objects.hash(id, name, bonusPoints, lastOrderDate);
        } else {
            return Objects.hash(id, name, bonusPoints);
        }
    }

    @Override
    public String toString() {
        if (Objects.equals(getCustomerType(), "REGULAR")) {
            return getCustomerType() + ", " + id + ", " + name
                    + ", " + bonusPoints + ", " + lastOrderDate;
        } else {
            return getCustomerType() + ", " + id + ", " + name + ", " + bonusPoints;
        }
    }
}