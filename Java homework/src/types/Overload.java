package types;

public class Overload {

    public static void main(String[] args) {
        add(2L, 3L);
        add(2, 3);
        add("23", "3545");
    }

    public static long add(long x, long y) {
        System.out.println("Adding longs");
        return x + y;
    }

    public static int add(int x, int y) {
        System.out.println("Adding integers");
        return x + y;
    }

    public static long add(String x, String y) {
        System.out.println("Adding numbers from strings");
        return Long.parseLong(x) + Long.parseLong(y);
    }

}
