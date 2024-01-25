package generics.cart;

public class CartEntry<T> {

    private final T cartEntry;
    private Integer quantity;

    public CartEntry(T cartEntry, Integer quantity) {
        this.cartEntry = cartEntry;
        this.quantity = quantity;
    }

    public T getCartEntry() {
        return cartEntry;
    }

    public Integer getQuantity() {
        return quantity;
    }

    public void setQuantity(Integer quantity) {
        this.quantity = quantity;
    }
}