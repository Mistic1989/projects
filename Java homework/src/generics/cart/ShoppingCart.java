package generics.cart;

import java.util.*;

public class ShoppingCart<T extends CartItem> {

    public static void main(String[] args) {
        ShoppingCart<Service> cart = new ShoppingCart<>();

        cart.add(new Service("s1", 3.0));
        cart.add(new Service("s2", 2.0));

        System.out.println(cart.getTotal());
    }

    private final List<CartEntry<T>> result = new ArrayList<>();
    private final LinkedList<Double> discounts = new LinkedList<>();


    public void add(T item) {
        if (!contains(item.getId())) {
            result.add(new CartEntry<T>(item, 1));
        } else {
            for (CartEntry<T> entry : result) {
                if (Objects.equals(entry.getCartEntry().getId(), item.getId())) {
                    entry.setQuantity(entry.getQuantity() + 1);
                    break;
                }
            }
        }
    }

    public void removeById(String id) {
        for (CartEntry<T> entry : result) {
            if (Objects.equals(entry.getCartEntry().getId(), id)) {
                result.remove(entry);
                break;
            }
        }
    }

    public Double getTotal() {
        Double sum = 0.0;
        for (CartEntry<T> entry : result) {
            sum += entry.getCartEntry().getPrice() * entry.getQuantity();
        }
        if (!discounts.isEmpty()) {
            for (Double discount : discounts) {
                sum = sum - (sum * (discount / 100));
            }
        }

        return sum;
    }

    public void increaseQuantity(String id) {
        for (CartEntry<T> entry : result) {
            if (Objects.equals(entry.getCartEntry().getId(), id)) {
                entry.setQuantity(entry.getQuantity() + 1);
            }
        }
    }

    public void applyDiscountPercentage(Double discount) {
        discounts.add(discount);
    }

    public void removeLastDiscount() {
        discounts.remove(discounts.getLast());
    }


    public void addAll(List<T> items) {
        for (T item : items) {
            add(item);
        }
    }

    public boolean contains(String str) {
        for (CartEntry<T> entry : result) {
            if (Objects.equals(entry.getCartEntry().getId(), str)) {
                return true;
            }
        }

        return false;
    }

    @Override
    public String toString() {

        LinkedHashSet<ArrayList<String>> set = new LinkedHashSet<>();
        String resultString = "";

        for (CartEntry<T> entry : result) {
            ArrayList<String> temp = new ArrayList<>();
            temp.add(entry.getCartEntry().getId());
            temp.add(entry.getCartEntry().getPrice().toString());
            temp.add(entry.getQuantity().toString());
            set.add(temp);
        }

        if (set.size() == 1) {
            for (ArrayList<String> arrayList : set) {
                return arrayList.toString().replace("[", "(").replace("]", ")");
            }
        } else {
            Integer index = 0;
            for (ArrayList<String> arrayList : set) {
                String temp = arrayList.toString().replace("[", "(")
                                                  .replace("]", ")");
                if (index == set.size() - 1) {
                    resultString += temp;
                    break;
                }
                resultString += temp + ", ";
                index++;
            }
        }

        return resultString;
    }
}